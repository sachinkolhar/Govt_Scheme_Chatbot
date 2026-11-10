"""CSV-first, non-destructive validation for label adjudication decisions."""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[2]
DECISIONS_PATH = SCRIPT_DIR / "label_decisions.csv"
SOURCE_WORKSHEET_PATH = ROOT_DIR / "backend/evaluation/label_audit_reports/manual_review_worksheet.csv"
DATASET_PATH = ROOT_DIR / "dataset/govt_schemes.csv"
EXPECTED_QUERY_COUNT = 40
EXPECTED_CANDIDATES_PER_QUERY = 3
EXPECTED_CANDIDATE_COUNT = 120
ALLOWED_DECISIONS = {
    "verified_match",
    "verified_no_match",
    "ambiguous",
    "dataset_missing",
    "needs_external_source_review",
}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_SECOND_REVIEW_STATUS = {"pending", "complete", "unresolved"}
REQUIRED_COLUMNS = {
    "query_number",
    "query_text",
    "source_expected_match",
    "candidate_rank",
    "candidate_dataset_row_index",
    "candidate_slug",
    "decision",
    "verified_dataset_slug",
    "rationale",
    "evidence_reference",
    "reviewer_id",
    "confidence",
    "second_review_status",
    "notes",
}
SOURCE_REQUIRED_COLUMNS = {
    "query_number",
    "query",
    "original_expected_scheme",
    "status",
    *{f"candidate_{rank}_{field}" for rank in (1, 2, 3) for field in ("dataset_row_index", "slug")},
}
PROVENANCE_NOTE_PREFIX = "Source candidate from manual_review_worksheet.csv"


def field(row: dict[str, str], name: str) -> str:
    return row.get(name, "").strip()


def load_csv(path: Path) -> tuple[list[dict[str, str]], set[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), set(reader.fieldnames or [])


def check(name: str, passed: bool, detail: str, errors: list[str]) -> None:
    print(f"{'PASS' if passed else 'FAIL'}: {name} - {detail}")
    if not passed:
        errors.append(f"{name}: {detail}")


def source_structure(errors: list[str]) -> tuple[set[int], set[tuple[int, int, int, str]]]:
    rows, columns = load_csv(SOURCE_WORKSHEET_PATH)
    missing = sorted(SOURCE_REQUIRED_COLUMNS - columns)
    check("source worksheet schema", not missing, f"missing={missing}", errors)
    if missing:
        return set(), set()
    pending = [row for row in rows if field(row, "status") == "pending_review"]
    query_numbers: list[int] = []
    source_keys: set[tuple[int, int, int, str]] = set()
    per_query: defaultdict[int, list[tuple[int, int, str]]] = defaultdict(list)
    parse_errors: list[str] = []
    for row in pending:
        try:
            query_number = int(field(row, "query_number"))
        except ValueError:
            parse_errors.append(field(row, "query_number"))
            continue
        query_numbers.append(query_number)
        for rank in range(1, 4):
            try:
                index = int(field(row, f"candidate_{rank}_dataset_row_index"))
            except ValueError:
                parse_errors.append(f"query {query_number} rank {rank}")
                continue
            slug = field(row, f"candidate_{rank}_slug")
            per_query[query_number].append((rank, index, slug))
            key = (query_number, rank, index, slug)
            source_keys.add(key)
    query_set = set(query_numbers)
    check("source pending query count", len(pending) == EXPECTED_QUERY_COUNT, f"found={len(pending)}", errors)
    check("source pending query numbers unique", len(query_set) == len(query_numbers), f"unique={len(query_set)}", errors)
    check("source candidate total", len(source_keys) == EXPECTED_CANDIDATE_COUNT, f"found={len(source_keys)}", errors)
    check(
        "source candidates per query",
        set(query_set) == set(per_query) and all(len(items) == 3 for items in per_query.values()),
        "exactly three source candidates per pending query",
        errors,
    )
    check(
        "source candidate ranks",
        all({rank for rank, _, _ in items} == {1, 2, 3} for items in per_query.values()),
        "every source query has ranks {1, 2, 3}",
        errors,
    )
    check("source candidate fields parse", not parse_errors, f"invalid={parse_errors[:5]}", errors)
    return query_set, source_keys


def dataset_traceability(
    rows: list[dict[str, str]],
    errors: list[str],
) -> defaultdict[int, set[str]]:
    dataset = pd.read_csv(DATASET_PATH).fillna("")
    candidate_slugs: defaultdict[int, set[str]] = defaultdict(set)
    index_errors: list[str] = []
    slug_errors: list[str] = []
    for row_number, row in enumerate(rows, start=2):
        try:
            query_number = int(field(row, "query_number"))
            dataset_index = int(field(row, "candidate_dataset_row_index"))
        except ValueError:
            continue
        slug = field(row, "candidate_slug")
        candidate_slugs[query_number].add(slug)
        if dataset_index < 0 or dataset_index >= len(dataset):
            index_errors.append(f"row {row_number}: {dataset_index}")
            continue
        current_slug = str(dataset.iloc[dataset_index].get("slug", "")).strip()
        if slug != current_slug:
            slug_errors.append(f"row {row_number}: {slug!r}!={current_slug!r}")
    check("dataset candidate indices in range", not index_errors, f"invalid={index_errors[:5]}", errors)
    check("dataset candidate slugs traceable", not slug_errors, f"mismatches={slug_errors[:5]}", errors)
    return candidate_slugs


def validate(rows: list[dict[str, str]]) -> tuple[list[str], list[str], dict[str, object]]:
    structural_errors: list[str] = []
    semantic_errors: list[str] = []
    diagnostics: dict[str, object] = {}

    _, columns = load_csv(DECISIONS_PATH)
    check("decision CSV schema", REQUIRED_COLUMNS.issubset(columns), f"missing={sorted(REQUIRED_COLUMNS - columns)}", structural_errors)
    if not REQUIRED_COLUMNS.issubset(columns):
        return structural_errors, semantic_errors, diagnostics

    source_queries, source_keys = source_structure(structural_errors)
    query_rows: defaultdict[int, list[tuple[int, dict[str, str]]]] = defaultdict(list)
    template_keys: set[tuple[int, int, int, str]] = set()
    candidate_slugs: defaultdict[int, set[str]] = defaultdict(set)
    parse_errors: list[str] = []
    negative_indices: list[str] = []
    for row_number, row in enumerate(rows, start=2):
        try:
            query_number = int(field(row, "query_number"))
            rank = int(field(row, "candidate_rank"))
            dataset_index = int(field(row, "candidate_dataset_row_index"))
        except ValueError:
            parse_errors.append(f"row {row_number}")
            continue
        slug = field(row, "candidate_slug")
        key = (query_number, rank, dataset_index, slug)
        if key in template_keys:
            structural_errors.append(f"row {row_number}: duplicate candidate key {key}")
        template_keys.add(key)
        query_rows[query_number].append((row_number, row))
        candidate_slugs[query_number].add(slug)
        if dataset_index < 0:
            negative_indices.append(f"row {row_number}: {dataset_index}")
        status = field(row, "second_review_status")
        if status not in ALLOWED_SECOND_REVIEW_STATUS:
            structural_errors.append(f"row {row_number}: invalid second_review_status {status!r}")
    check("decision row count", len(rows) == EXPECTED_CANDIDATE_COUNT, f"found={len(rows)}", structural_errors)
    check("decision query set", set(query_rows) == source_queries, f"missing={sorted(source_queries - set(query_rows))}, extra={sorted(set(query_rows) - source_queries)}", structural_errors)
    check("decision rows per query", all(len(items) == 3 for items in query_rows.values()), "exactly three rows per query", structural_errors)
    check("decision rank sets", all({int(field(row, "candidate_rank")) for _, row in items} == {1, 2, 3} for items in query_rows.values()), "every query has ranks {1, 2, 3}", structural_errors)
    check("decision row parsing", not parse_errors, f"invalid={parse_errors[:5]}", structural_errors)
    check("nonnegative dataset indices", not negative_indices, f"invalid={negative_indices[:5]}", structural_errors)
    check("decision keys unique", len(template_keys) == len(rows), f"unique={len(template_keys)}", structural_errors)
    check("decision keys match source", template_keys == source_keys, f"missing={len(source_keys - template_keys)}, extra={len(template_keys - source_keys)}", structural_errors)
    current_slugs = dataset_traceability(rows, structural_errors)

    multiple_matches: list[int] = []
    partially_reviewed: list[int] = []
    mixed_statuses: list[int] = []
    conflicting_patterns: list[int] = []
    status_counts_by_query: dict[int, dict[str, int]] = {}
    for query_number, grouped in sorted(query_rows.items()):
        decisions = [field(row, "decision") for _, row in grouped]
        statuses = [field(row, "second_review_status") for _, row in grouped]
        status_counts_by_query[query_number] = dict(Counter(statuses))
        nonblank = [decision for decision in decisions if decision]
        if sum(decision == "verified_match" for decision in decisions) > 1:
            multiple_matches.append(query_number)
        if nonblank and any(not decision for decision in decisions):
            partially_reviewed.append(query_number)
        if len(set(statuses)) > 1:
            mixed_statuses.append(query_number)
        if len(set(nonblank)) > 1:
            conflicting_patterns.append(query_number)
    diagnostics.update({
        "partially_reviewed_queries": partially_reviewed,
        "mixed_review_status_queries": mixed_statuses,
        "multiple_verified_match_queries": multiple_matches,
        "conflicting_decision_pattern_queries": conflicting_patterns,
        "status_counts_by_query": status_counts_by_query,
    })
    if multiple_matches:
        semantic_errors.append(f"queries with multiple verified_match rows: {multiple_matches}")

    for row_number, row in enumerate(rows, start=2):
        decision = field(row, "decision")
        status = field(row, "second_review_status")
        required_review_fields = [
            field(row, name)
            for name in ("rationale", "evidence_reference", "reviewer_id", "confidence")
        ]
        verified_slug = field(row, "verified_dataset_slug")
        notes = field(row, "notes")
        if not decision:
            if status != "pending":
                semantic_errors.append(f"row {row_number}: blank decision must remain pending")
            if any(required_review_fields) or verified_slug or (notes and not notes.startswith(PROVENANCE_NOTE_PREFIX)):
                semantic_errors.append(f"row {row_number}: partially populated reviewer fields with blank decision")
            continue
        if decision not in ALLOWED_DECISIONS:
            semantic_errors.append(f"row {row_number}: unsupported decision {decision!r}")
            continue
        if not field(row, "rationale") or not field(row, "evidence_reference") or not field(row, "reviewer_id") or field(row, "confidence").casefold() not in ALLOWED_CONFIDENCE:
            semantic_errors.append(f"row {row_number}: reviewed decision lacks required rationale, evidence, reviewer, or confidence")
        if status == "pending":
            print(f"INCOMPLETE: row {row_number} has a reviewed decision with pending second_review_status")
        if status == "complete" and not all(required_review_fields):
            semantic_errors.append(f"row {row_number}: complete status requires all required review fields")
        if status == "unresolved" and not all(required_review_fields):
            semantic_errors.append(f"row {row_number}: unresolved status requires all required review fields")
        try:
            query_number = int(field(row, "query_number"))
        except ValueError:
            continue
        if decision == "verified_match":
            if not verified_slug:
                semantic_errors.append(f"row {row_number}: verified_match requires verified_dataset_slug")
            elif verified_slug not in candidate_slugs[query_number] or verified_slug not in current_slugs[query_number]:
                semantic_errors.append(f"row {row_number}: verified slug is not a current candidate dataset slug")
        elif verified_slug:
            semantic_errors.append(f"row {row_number}: verified_dataset_slug is only allowed for verified_match")
        if decision == "dataset_missing":
            print(f"LIMIT: row {row_number} dataset_missing evidence must establish absence from the current dataset; rejecting candidates alone is insufficient")
        if decision == "ambiguous":
            print(f"LIMIT: row {row_number} ambiguous rationale must describe competing interpretations or lack of specificity")

    return structural_errors, semantic_errors, diagnostics


def main() -> int:
    rows, columns = load_csv(DECISIONS_PATH)
    structural_errors, semantic_errors, diagnostics = validate(rows)
    counts = Counter(field(row, "decision") or "blank" for row in rows)
    statuses = Counter(field(row, "second_review_status") or "blank" for row in rows)
    print(f"Rows read: {len(rows)}")
    print("Decision counts:")
    for name in ["blank", *sorted(ALLOWED_DECISIONS)]:
        print(f"  {name}: {counts.get(name, 0)}")
    print("Second-review status counts:")
    for name in [*sorted(ALLOWED_SECOND_REVIEW_STATUS), "blank"]:
        print(f"  {name}: {statuses.get(name, 0)}")
    print("Partially reviewed queries:", diagnostics.get("partially_reviewed_queries", []))
    print("Mixed review-status queries:", diagnostics.get("mixed_review_status_queries", []))
    print("Multiple verified-match queries:", diagnostics.get("multiple_verified_match_queries", []))
    print("Conflicting decision-pattern queries:", diagnostics.get("conflicting_decision_pattern_queries", []))
    print("Status counts by query:", diagnostics.get("status_counts_by_query", {}))
    print(f"Structural errors: {len(structural_errors)}")
    for error in structural_errors:
        print(f"STRUCTURAL ERROR: {error}")
    print(f"Semantic-field validation errors: {len(semantic_errors)}")
    for error in semantic_errors:
        print(f"SEMANTIC ERROR: {error}")
    print("Retrieval metrics calculated: no")
    return 1 if structural_errors or semantic_errors else 0


if __name__ == "__main__":
    sys.exit(main())
