"""Create non-destructive manual-review reports from ``label_audit.csv``."""

import argparse
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import pandas as pd


STOP_WORDS = {
    "and", "for", "of", "the", "to", "scheme", "yojana", "programme",
    "program", "national", "pradhan", "mantri", "government", "india",
}


def normalize(value: Any) -> str:
    return " ".join(str(value or "").casefold().replace("-", " ").split())


def token_set(value: Any) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", normalize(value))
        if token not in STOP_WORDS and len(token) > 1
    }


def name_scores(expected: Any, candidate: Any) -> tuple[float, float, float]:
    expected_tokens = token_set(expected)
    candidate_tokens = token_set(candidate)
    union = expected_tokens | candidate_tokens
    overlap = len(expected_tokens & candidate_tokens) / len(union) if union else 0.0
    sequence = SequenceMatcher(None, normalize(expected), normalize(candidate)).ratio()
    combined = max(overlap, sequence * 0.8)
    return combined, overlap, sequence


def parse_candidate_names(value: Any) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    for item in str(value or "").split("; "):
        match = re.match(r"^(.*) \[([^\]]+)\]$", item)
        if match:
            candidates.append((match.group(1), match.group(2)))
    return candidates


def trace_candidates(audit: pd.DataFrame, dataset: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    dataset_by_slug = {
        normalize(row["slug"]): (int(index), row)
        for index, row in dataset.iterrows()
        if normalize(row["slug"])
    }

    for _, record in audit.iterrows():
        if record["label_class"] != "positive":
            continue
        for candidate_name, candidate_slug in parse_candidate_names(record["possible_dataset_specific_matches"]):
            traced = dataset_by_slug.get(normalize(candidate_slug))
            if traced is None:
                raise ValueError(f"Candidate slug cannot be traced to dataset: {candidate_slug}")
            dataset_index, dataset_row = traced
            if normalize(dataset_row["scheme_name"]) != normalize(candidate_name):
                raise ValueError(f"Candidate name/slug mismatch in dataset: {candidate_slug}")
            combined, overlap, sequence = name_scores(record["expected_scheme"], candidate_name)
            rows.append({
                "query_number": int(record["query_number"]),
                "query": record["query"],
                "expected_scheme": record["expected_scheme"],
                "dataset_row_index": dataset_index,
                "dataset_slug": dataset_row["slug"],
                "dataset_scheme_name": dataset_row["scheme_name"],
                "name_similarity_score": combined,
                "token_jaccard_similarity": overlap,
                "sequence_similarity": sequence,
                "faiss_distance": "unavailable in label_audit.csv",
                "candidate_approved": False,
                "traceability_verified": True,
            })
    return pd.DataFrame(rows)


def classify_mapping(record: pd.Series, candidate_count: int) -> str:
    if bool(record["expected_scheme_exists_in_dataset"]):
        return "exact_mapping"
    if candidate_count == 0:
        return "remove_from_evaluation_missing_ground_truth"
    if candidate_count == 1:
        return "explicit_canonical_mapping_required"
    return "multiple_candidate_review_required"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    parser.add_argument("--audit", type=Path, default=script_dir / "label_audit.csv")
    parser.add_argument("--dataset", type=Path, default=root_dir / "dataset" / "govt_schemes.csv")
    parser.add_argument("--output-dir", type=Path, default=script_dir / "label_audit_reports")
    args = parser.parse_args()

    audit = pd.read_csv(args.audit).fillna("")
    dataset = pd.read_csv(args.dataset).fillna("")
    candidates = trace_candidates(audit, dataset)
    candidate_counts = candidates.groupby("query_number").size().to_dict() if not candidates.empty else {}

    mapping_rows: list[dict[str, Any]] = []
    for _, record in audit[audit["label_class"] == "positive"].iterrows():
        count = int(candidate_counts.get(int(record["query_number"]), 0))
        category = classify_mapping(record, count)
        mapping_rows.append({
            "query_number": int(record["query_number"]),
            "query": record["query"],
            "expected_scheme": record["expected_scheme"],
            "mapping_category": category,
            "candidate_count": count,
            "matching_dataset_row_indices": record["matching_dataset_row_indices"],
            "matching_scheme_slugs": record["matching_scheme_slugs"],
            "matching_scheme_names": record["matching_scheme_names"],
            "traceability_status": "verified" if bool(record["expected_scheme_exists_in_dataset"]) else "candidate records verified; equivalence unresolved",
            "automatic_approval": False,
            "manual_action": "Review source evidence and explicitly approve, remap, or remove",
        })

    mapping = pd.DataFrame(mapping_rows)
    category_order = [
        "exact_mapping",
        "explicit_canonical_mapping_required",
        "multiple_candidate_review_required",
        "remove_from_evaluation_missing_ground_truth",
    ]
    category_summary = pd.DataFrame({"mapping_category": category_order})
    category_counts = mapping["mapping_category"].value_counts() if not mapping.empty else pd.Series(dtype="int64")
    category_summary["query_count"] = category_summary["mapping_category"].map(category_counts).fillna(0).astype(int)
    category_summary["automatic_approval"] = False
    category_summary["decision_rule"] = [
        "Exact scheme_name or slug exists; still preserve review trail",
        "One traceable candidate exists; explicit human canonical mapping required",
        "Two or more traceable candidates exist; choose only with source evidence",
        "No traceable ground-truth record exists; exclude unless labels are repaired",
    ]
    issue_rows: list[dict[str, Any]] = []
    for issue in sorted({issue for value in audit["label_issues"] for issue in str(value).split(";") if issue}):
        subset = audit[audit["label_issues"].str.contains(issue, regex=False)]
        issue_rows.append({
            "label_issue": issue,
            "query_count": len(subset),
            "query_numbers": ";".join(str(value) for value in subset["query_number"]),
            "queries": " | ".join(str(value) for value in subset["query"]),
            "manual_review_required": True,
        })
    issue_report = pd.DataFrame(issue_rows)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    issue_report.to_csv(args.output_dir / "manual_review_by_issue.csv", index=False)
    mapping.to_csv(args.output_dir / "label_mapping_review.csv", index=False)
    category_summary.to_csv(args.output_dir / "mapping_category_summary.csv", index=False)
    candidates.to_csv(args.output_dir / "positive_candidate_records.csv", index=False)

    print(f"Issue groups: {len(issue_report)}")
    print(f"Positive mapping rows: {len(mapping)}")
    print(f"Candidate records: {len(candidates)}")
    print("FAISS distances: unavailable in label_audit.csv; candidate scores are name similarity only")
    print(f"Wrote reports to {args.output_dir}")


if __name__ == "__main__":
    main()