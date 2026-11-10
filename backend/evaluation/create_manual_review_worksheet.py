"""Create a blank reviewer worksheet from existing label-audit reports."""

import argparse
from pathlib import Path

import pandas as pd


REVIEW_DECISIONS = {
    "verified_exact_match",
    "verified_canonical_mapping",
    "multiple_plausible_candidates",
    "no_valid_dataset_match",
    "insufficient_evidence",
}


def validate_candidate(candidate: pd.Series, dataset: pd.DataFrame) -> None:
    row_index = int(candidate["dataset_row_index"])
    slug = str(candidate["dataset_slug"])
    if row_index < 0 or row_index >= len(dataset):
        raise ValueError(f"Candidate row index is out of range: {row_index}")

    slug_matches = dataset.index[
        dataset["slug"].astype(str).str.casefold() == slug.casefold()
    ].tolist()
    if len(slug_matches) != 1:
        raise ValueError(
            f"Candidate slug {slug!r} maps to {len(slug_matches)} dataset rows; "
            "expected exactly one."
        )
    if slug_matches[0] != row_index:
        raise ValueError(
            f"Candidate slug {slug!r} maps to row {slug_matches[0]}, "
            f"not row {row_index}."
        )

    dataset_row = dataset.iloc[row_index]
    if str(dataset_row["scheme_name"]) != str(candidate["dataset_scheme_name"]):
        raise ValueError(f"Candidate name mismatch for slug {slug!r}")


def build_worksheet(mapping: pd.DataFrame, candidates: pd.DataFrame, dataset: pd.DataFrame) -> pd.DataFrame:
    unresolved = mapping[mapping["mapping_category"] != "exact_mapping"].copy()
    if len(unresolved) != 40:
        raise ValueError(f"Expected 40 unresolved positive queries, found {len(unresolved)}")

    rows: list[dict[str, object]] = []
    for _, mapping_row in unresolved.iterrows():
        query_number = int(mapping_row["query_number"])
        group = candidates[candidates["query_number"] == query_number].copy()
        if len(group) != 3:
            raise ValueError(
                f"Query {query_number} has {len(group)} candidates; expected exactly 3."
            )
        group = group.reset_index(drop=True)
        for _, candidate in group.iterrows():
            validate_candidate(candidate, dataset)

        row: dict[str, object] = {
            "query_number": query_number,
            "query": mapping_row["query"],
            "original_expected_scheme": mapping_row["expected_scheme"],
        }
        for position, (_, candidate) in enumerate(group.iterrows(), start=1):
            prefix = f"candidate_{position}"
            row[f"{prefix}_dataset_row_index"] = int(candidate["dataset_row_index"])
            row[f"{prefix}_slug"] = candidate["dataset_slug"]
            row[f"{prefix}_scheme_name"] = candidate["dataset_scheme_name"]
            row[f"{prefix}_name_similarity_score"] = candidate["name_similarity_score"]

        row["reviewer_decision"] = ""
        row["verified_dataset_slug"] = ""
        row["reviewer_reason"] = ""
        row["status"] = "pending_review"
        rows.append(row)

    worksheet = pd.DataFrame(rows)
    if worksheet["query_number"].duplicated().any():
        raise ValueError("Worksheet contains duplicate query numbers")
    if set(worksheet["status"]) != {"pending_review"}:
        raise ValueError("Worksheet status was not initialized to pending_review")
    if worksheet[["reviewer_decision", "verified_dataset_slug", "reviewer_reason"]].isna().any().any():
        raise ValueError("Reviewer fields must be blank, not null")
    if REVIEW_DECISIONS.intersection(set(worksheet["reviewer_decision"])):
        raise ValueError("Reviewer decisions must not be pre-filled")
    return worksheet


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    report_dir = script_dir / "label_audit_reports"
    parser.add_argument("--mapping", type=Path, default=report_dir / "label_mapping_review.csv")
    parser.add_argument("--candidates", type=Path, default=report_dir / "positive_candidate_records.csv")
    parser.add_argument("--dataset", type=Path, default=root_dir / "dataset" / "govt_schemes.csv")
    parser.add_argument("--output", type=Path, default=report_dir / "manual_review_worksheet.csv")
    args = parser.parse_args()

    mapping = pd.read_csv(args.mapping).fillna("")
    candidates = pd.read_csv(args.candidates).fillna("")
    dataset = pd.read_csv(args.dataset).fillna("")
    worksheet = build_worksheet(mapping, candidates, dataset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    worksheet.to_csv(args.output, index=False)
    print(f"Created {len(worksheet)} pending-review rows")
    print(f"Reviewer decisions filled: {int(worksheet['reviewer_decision'].ne('').sum())}")
    print(f"Candidate identifiers validated: {len(worksheet) * 3}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()