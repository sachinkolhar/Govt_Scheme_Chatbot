"""Generate a non-destructive reviewer report for unresolved label adjudication."""

from __future__ import annotations

import csv
import html
import sys
from pathlib import Path
from typing import Any

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[2]
WORKSHEET_PATH = ROOT_DIR / "backend/evaluation/label_audit_reports/manual_review_worksheet.csv"
TEMPLATE_PATH = SCRIPT_DIR / "label_decisions.csv"
DATASET_PATH = ROOT_DIR / "dataset/govt_schemes.csv"
REPORT_PATH = SCRIPT_DIR / "reviewer_adjudication_report.md"

EXPECTED_QUERY_COUNT = 40
EXPECTED_CANDIDATES_PER_QUERY = 3
EXPECTED_CANDIDATE_COUNT = EXPECTED_QUERY_COUNT * EXPECTED_CANDIDATES_PER_QUERY
DECISION_FIELDS = (
    "decision",
    "verified_dataset_slug",
    "rationale",
    "evidence_reference",
    "reviewer_id",
    "confidence",
)
SOURCE_REQUIRED_COLUMNS = {
    "query_number",
    "query",
    "original_expected_scheme",
    "status",
    *{f"candidate_{rank}_{field}" for rank in (1, 2, 3) for field in ("dataset_row_index", "slug")},
}
TEMPLATE_REQUIRED_COLUMNS = {
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

REPORT_FIELDS = (
    "query number",
    "query text",
    "original source label",
    "candidate rank",
    "candidate dataset row index",
    "candidate slug",
    "scheme name/title",
    "details",
    "eligibility",
    "benefits/scope",
    "source or official-reference fields",
)


def markdown_value(value: Any, field: str, columns: set[str]) -> str:
    if field not in columns:
        return "[FIELD NOT PRESENT IN DATASET]"
    if pd.isna(value) or str(value).strip() == "":
        return "[FIELD PRESENT BUT EMPTY]"
    return str(value).strip()


def source_reference_columns(columns: list[str]) -> list[str]:
    tokens = ("source", "official", "reference", "url", "uri", "link", "website")
    excluded = {"source_expected_match"}
    return [
        column
        for column in columns
        if column not in excluded and any(token in column.casefold() for token in tokens)
    ]


def safe_text(value: Any) -> str:
    return html.escape(str(value), quote=False)


def load_pending_rows() -> list[dict[str, str]]:
    rows = list(csv.DictReader(WORKSHEET_PATH.open(encoding="utf-8-sig", newline="")))
    pending = [row for row in rows if row.get("status") == "pending_review"]
    if len(pending) != EXPECTED_QUERY_COUNT:
        raise ValueError(f"Expected {EXPECTED_QUERY_COUNT} pending queries, found {len(pending)}")
    query_numbers = [int(row["query_number"]) for row in pending]
    if len(set(query_numbers)) != EXPECTED_QUERY_COUNT:
        raise ValueError("Pending worksheet contains duplicate query numbers")
    return sorted(pending, key=lambda row: int(row["query_number"]))


def load_template_keys() -> set[tuple[int, int, str, str]]:
    rows = list(csv.DictReader(TEMPLATE_PATH.open(encoding="utf-8-sig", newline="")))
    if len(rows) != EXPECTED_CANDIDATE_COUNT:
        raise ValueError(f"Expected {EXPECTED_CANDIDATE_COUNT} template rows, found {len(rows)}")
    keys: set[tuple[int, int, str, str]] = set()
    for row in rows:
        key = (
            int(row["query_number"]),
            int(row["candidate_rank"]),
            row["candidate_dataset_row_index"],
            row["candidate_slug"],
        )
        if key in keys:
            raise ValueError(f"Duplicate template candidate row: {key}")
        keys.add(key)
        if any(row[field].strip() for field in ("decision", "verified_dataset_slug", "rationale", "evidence_reference", "reviewer_id", "confidence")):
            raise ValueError(f"Template contains prefilled reviewer content for {key}")
        if row["second_review_status"].strip() != "pending":
            raise ValueError(f"Template second-review status is not pending for {key}")
    return keys


def validate_inputs() -> bool:
    """Run every structural check and print each result independently."""
    errors: list[str] = []

    def check(name: str, passed: bool, detail: str) -> None:
        print(f"{'PASS' if passed else 'FAIL'}: {name} - {detail}")
        if not passed:
            errors.append(name)

    source_reader = csv.DictReader(WORKSHEET_PATH.open(encoding="utf-8-sig", newline=""))
    source_columns = set(source_reader.fieldnames or [])
    check(
        "source worksheet required columns",
        SOURCE_REQUIRED_COLUMNS.issubset(source_columns),
        f"missing={sorted(SOURCE_REQUIRED_COLUMNS - source_columns)}",
    )
    if not SOURCE_REQUIRED_COLUMNS.issubset(source_columns):
        print(f"Validation errors: {len(errors)}")
        return False
    source_rows = list(source_reader)
    pending = [row for row in source_rows if row.get("status") == "pending_review"]
    query_number_errors: list[str] = []
    query_numbers: list[int] = []
    for row in pending:
        try:
            query_numbers.append(int(row["query_number"]))
        except ValueError:
            query_number_errors.append(row.get("query_number", ""))
    unique_queries = set(query_numbers)
    check(
        "pending query count",
        len(pending) == EXPECTED_QUERY_COUNT and len(unique_queries) == EXPECTED_QUERY_COUNT,
        f"found {len(pending)} rows and {len(unique_queries)} unique query numbers; expected {EXPECTED_QUERY_COUNT}",
    )
    check("pending query numbers are valid integers", not query_number_errors, f"invalid={query_number_errors}")
    if query_number_errors:
        print(f"Validation errors: {len(errors)}")
        return False

    source_keys: set[tuple[int, int, str, str]] = set()
    source_candidate_counts: dict[int, int] = {}
    source_rank_sets: dict[int, set[int]] = {}
    source_index_errors: list[str] = []
    source_slug_errors: list[str] = []
    dataset = pd.read_csv(DATASET_PATH).fillna("")
    for row in pending:
        query_number = int(row["query_number"])
        source_candidate_counts[query_number] = 0
        source_rank_sets[query_number] = set()
        for rank in range(1, EXPECTED_CANDIDATES_PER_QUERY + 1):
            index_value = row.get(f"candidate_{rank}_dataset_row_index", "").strip()
            slug = row.get(f"candidate_{rank}_slug", "").strip()
            if not index_value or not slug:
                continue
            source_candidate_counts[query_number] += 1
            source_rank_sets[query_number].add(rank)
            try:
                dataset_index = int(index_value)
            except ValueError:
                source_index_errors.append(f"query {query_number} rank {rank}: non-integer index")
                continue
            source_keys.add((query_number, rank, str(dataset_index), slug))
            if not 0 <= dataset_index < len(dataset):
                source_index_errors.append(f"query {query_number} rank {rank}: index {dataset_index} out of range")
                continue
            dataset_slug = str(dataset.iloc[dataset_index].get("slug", "")).strip()
            if dataset_slug != slug:
                source_slug_errors.append(
                    f"query {query_number} rank {rank}: worksheet={slug!r}, dataset={dataset_slug!r}"
                )

    check(
        "source candidates per pending query",
        all(count == EXPECTED_CANDIDATES_PER_QUERY for count in source_candidate_counts.values()),
        f"counts={sorted(set(source_candidate_counts.values()))}; expected 3 for every query",
    )
    check(
        "source candidate total",
        sum(source_candidate_counts.values()) == EXPECTED_CANDIDATE_COUNT,
        f"found {sum(source_candidate_counts.values())}; expected {EXPECTED_CANDIDATE_COUNT}",
    )
    check(
        "source candidate ranks",
        all(ranks == {1, 2, 3} for ranks in source_rank_sets.values()),
        "every pending query has rank set {1, 2, 3}",
    )
    check("source candidate keys unique", len(source_keys) == sum(source_candidate_counts.values()), f"keys={len(source_keys)}")
    check("candidate indices in range", not source_index_errors, "all source indices are valid dataset positions")
    check("candidate slugs match dataset", not source_slug_errors, "all source slugs match their current dataset rows")

    template_reader = csv.DictReader(TEMPLATE_PATH.open(encoding="utf-8-sig", newline=""))
    template_columns = set(template_reader.fieldnames or [])
    check(
        "decision template required columns",
        TEMPLATE_REQUIRED_COLUMNS.issubset(template_columns),
        f"missing={sorted(TEMPLATE_REQUIRED_COLUMNS - template_columns)}",
    )
    if not TEMPLATE_REQUIRED_COLUMNS.issubset(template_columns):
        print(f"Validation errors: {len(errors)}")
        return False
    template_rows = list(template_reader)
    template_keys: set[tuple[int, int, str, str]] = set()
    template_query_counts: dict[int, int] = {}
    template_shape_ok = True
    template_rank_sets: dict[int, set[int]] = {}
    template_parse_errors: list[str] = []
    for row in template_rows:
        try:
            query_number = int(row["query_number"])
            rank = int(row["candidate_rank"])
            key = (
                query_number,
                rank,
                row["candidate_dataset_row_index"],
                row["candidate_slug"],
            )
        except (KeyError, ValueError):
            template_shape_ok = False
            template_parse_errors.append(str(row))
            continue
        template_keys.add(key)
        template_query_counts[query_number] = template_query_counts.get(query_number, 0) + 1
        template_rank_sets.setdefault(query_number, set()).add(rank)
    check(
        "decision template row count",
        len(template_rows) == EXPECTED_CANDIDATE_COUNT,
        f"found {len(template_rows)}; expected {EXPECTED_CANDIDATE_COUNT}",
    )
    check(
        "decision template rows per query",
        template_shape_ok and set(template_query_counts) == unique_queries and all(count == 3 for count in template_query_counts.values()),
        "exactly 3 template rows exist for every pending query",
    )
    check(
        "decision template ranks",
        template_shape_ok and all(ranks == {1, 2, 3} for ranks in template_rank_sets.values()),
        "every template query has rank set {1, 2, 3}",
    )
    check("decision template row keys parse", not template_parse_errors, f"invalid={len(template_parse_errors)}")
    check(
        "generated candidate keys in decision template",
        source_keys == template_keys,
        f"missing={len(source_keys - template_keys)}, extra={len(template_keys - source_keys)}",
    )
    decision_fields_blank = all(not row.get(field, "").strip() for row in template_rows for field in DECISION_FIELDS)
    check("decision fields blank", decision_fields_blank, "all decision and reviewer fields are blank")
    pending_status = all(row.get("second_review_status", "").strip() == "pending" for row in template_rows)
    check("second-review status pending", pending_status, "all template rows are pending")
    print(f"Validation errors: {len(errors)}")
    return not errors


def candidate_records(
    pending_rows: list[dict[str, str]], dataset: pd.DataFrame
) -> list[dict[str, Any]]:
    dataset_columns = set(dataset.columns)
    template_keys = load_template_keys()
    source_columns = source_reference_columns(list(dataset.columns))
    records: list[dict[str, Any]] = []

    for row in pending_rows:
        query_number = int(row["query_number"])
        for rank in range(1, EXPECTED_CANDIDATES_PER_QUERY + 1):
            index_key = f"candidate_{rank}_dataset_row_index"
            slug_key = f"candidate_{rank}_slug"
            if not row.get(index_key, "").strip() or not row.get(slug_key, "").strip():
                raise ValueError(f"Missing traceable candidate fields for query {query_number}, rank {rank}")
            dataset_index = int(float(row[index_key]))
            if dataset_index < 0 or dataset_index >= len(dataset):
                raise ValueError(f"Dataset row index out of range: {query_number}, rank {rank}")
            dataset_row = dataset.iloc[dataset_index]
            dataset_slug = str(dataset_row.get("slug", "")).strip()
            source_slug = row[slug_key].strip()
            if dataset_slug != source_slug:
                raise ValueError(
                    f"Candidate slug mismatch for query {query_number}, rank {rank}: "
                    f"worksheet={source_slug!r}, dataset={dataset_slug!r}"
                )
            key = (query_number, rank, str(dataset_index), source_slug)
            if key not in template_keys:
                raise ValueError(f"Candidate missing from decision template: {key}")
            source_refs = []
            for column in source_columns:
                source_refs.append(f"{column}: {markdown_value(dataset_row.get(column), column, dataset_columns)}")
            records.append(
                {
                    "query_number": query_number,
                    "query": row["query"],
                    "source_label": row["original_expected_scheme"],
                    "rank": rank,
                    "dataset_index": dataset_index,
                    "slug": source_slug,
                    "scheme_name": markdown_value(dataset_row.get("scheme_name"), "scheme_name", dataset_columns),
                    "details": markdown_value(dataset_row.get("details"), "details", dataset_columns),
                    "eligibility": markdown_value(dataset_row.get("eligibility"), "eligibility", dataset_columns),
                    "benefits": markdown_value(dataset_row.get("benefits"), "benefits", dataset_columns),
                    "source_refs": source_refs or ["No source or official-reference field is present in the dataset."],
                }
            )
    if len(records) != EXPECTED_CANDIDATE_COUNT:
        raise ValueError(f"Expected {EXPECTED_CANDIDATE_COUNT} candidate records, found {len(records)}")
    return records


def render_report(records: list[dict[str, Any]], dataset_columns: list[str]) -> str:
    grouped: dict[int, list[dict[str, Any]]] = {}
    for record in records:
        grouped.setdefault(record["query_number"], []).append(record)

    lines = [
        "# Reviewer Adjudication Report",
        "",
        "> **Warning:** `original_expected_scheme` is an unverified source label, not ground truth. Candidate rank, string similarity, traceability, FAISS distance, and dataset row counts must not be treated as semantic correctness. FAISS index-to-dataset row alignment is not verified.",
        "",
        "This report is generated from the pending rows in `backend/evaluation/label_audit_reports/manual_review_worksheet.csv`, the current `dataset/govt_schemes.csv`, and the blank `label_decisions.csv` template. It contains no prefilled decisions or reviewer conclusions.",
        "",
        f"- Pending queries: {len(grouped)}",
        f"- Candidate entries: {len(records)}",
        f"- Dataset fields inspected: {', '.join(dataset_columns)}",
        "- Missing versus empty fields: `[FIELD NOT PRESENT IN DATASET]` means the column does not exist; `[FIELD PRESENT BUT EMPTY]` means the column exists but the selected cell is blank.",
        "",
        "## Review Prompts",
        "",
        "After each candidate, complete the prompts without inferring from the source label or ranking:",
        "",
        "```text",
        "decision:",
        "verified_dataset_slug:",
        "rationale:",
        "evidence_reference:",
        "reviewer_id:",
        "confidence:",
        "second_review_status:",
        "notes:",
        "```",
        "",
    ]
    for query_number in sorted(grouped):
        query_records = grouped[query_number]
        first = query_records[0]
        lines.extend(
            [
                f"## Query {query_number}",
                "",
                f"- **Query text:** {safe_text(first['query'])}",
                f"- **Original source label (unverified):** {safe_text(first['source_label'])}",
                "- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.",
                "",
            ]
        )
        for record in sorted(query_records, key=lambda item: item["rank"]):
            lines.extend(
                [
                    f"### Candidate {record['rank']}",
                    "",
                    f"- **Candidate rank:** {record['rank']}",
                    f"- **Candidate dataset row index:** {record['dataset_index']}",
                    f"- **Candidate slug:** `{safe_text(record['slug'])}`",
                    f"- **Scheme name/title:** {safe_text(record['scheme_name'])}",
                    f"- **Details:** {safe_text(record['details'])}",
                    f"- **Eligibility:** {safe_text(record['eligibility'])}",
                    f"- **Benefits/scope:** {safe_text(record['benefits'])}",
                    "- **Source or official-reference fields:**",
                ]
            )
            lines.extend([f"  - {safe_text(reference)}" for reference in record["source_refs"]])
            lines.extend(
                [
                    "",
                    "**Reviewer fields**",
                    "",
                    "- decision:",
                    "- verified_dataset_slug:",
                    "- rationale:",
                    "- evidence_reference:",
                    "- reviewer_id:",
                    "- confidence:",
                    "- second_review_status:",
                    "- notes:",
                    "",
                ]
            )
    return "\n".join(lines)


def main() -> int:
    if not validate_inputs():
        return 1
    pending_rows = load_pending_rows()
    dataset = pd.read_csv(DATASET_PATH).fillna("")
    records = candidate_records(pending_rows, dataset)
    report = render_report(records, list(dataset.columns))
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Pending queries included: {len(pending_rows)}")
    print(f"Candidate entries included: {len(records)}")
    print("Automatic decisions made: 0")
    print("Traceability problems: 0")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT_DIR).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
