"""Audit retrieval-evaluation labels without changing the source data."""

import argparse
import json
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


def tokens(value: Any) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", normalize(value))
        if token not in STOP_WORDS and len(token) > 1
    }


def find_matches(expected: Any, dataset: pd.DataFrame) -> tuple[list[int], str]:
    label = normalize(expected)
    if not label:
        return [], "missing"

    matches: list[int] = []
    name_matches = dataset.index[dataset["scheme_name"].map(normalize) == label].tolist()
    slug_matches = dataset.index[dataset["slug"].map(normalize) == label].tolist()
    matches = sorted(set(name_matches + slug_matches))
    if name_matches and slug_matches:
        return matches, "scheme_name_and_slug"
    if name_matches:
        return matches, "scheme_name"
    if slug_matches:
        return matches, "slug"
    return [], "none"


def possible_dataset_names(expected: Any, dataset: pd.DataFrame, limit: int = 3) -> list[tuple[int, float]]:
    expected_tokens = tokens(expected)
    if not expected_tokens:
        return []

    candidates: list[tuple[int, float]] = []
    for index, row in dataset.iterrows():
        name = row["scheme_name"]
        name_tokens = tokens(name)
        overlap = len(expected_tokens & name_tokens) / len(expected_tokens | name_tokens)
        sequence = SequenceMatcher(None, normalize(expected), normalize(name)).ratio()
        score = max(overlap, sequence * 0.8)
        if score >= 0.35:
            candidates.append((int(index), score))
    return sorted(candidates, key=lambda item: item[1], reverse=True)[:limit]


def audit_labels(query_path: Path, dataset_path: Path) -> pd.DataFrame:
    queries = json.loads(query_path.read_text(encoding="utf-8"))
    dataset = pd.read_csv(dataset_path).fillna("")
    normalized_queries = [normalize(record.get("query")) for record in queries]
    duplicate_counts = pd.Series(normalized_queries).value_counts().to_dict()
    rows: list[dict[str, Any]] = []

    for position, record in enumerate(queries, start=1):
        query = record.get("query", "")
        expected_scheme = record.get("expected_scheme")
        expected_match = record.get("expected_match")
        expected_match_valid = isinstance(expected_match, bool)
        has_expected_scheme = bool(normalize(expected_scheme))
        matching_indices, match_type = find_matches(expected_scheme, dataset)
        possible = possible_dataset_names(expected_scheme, dataset) if has_expected_scheme else []

        issues: list[str] = []
        if not normalize(query):
            issues.append("missing_query")
        if not expected_match_valid:
            issues.append("expected_match_not_boolean")
        if expected_match is True and not has_expected_scheme:
            issues.append("positive_missing_expected_scheme")
        if expected_match is False and has_expected_scheme:
            issues.append("negative_has_expected_scheme")
        if expected_match is True and has_expected_scheme and not matching_indices:
            issues.append("positive_scheme_not_in_dataset")
        if expected_match is False and matching_indices:
            issues.append("negative_scheme_exists_in_dataset")
        if duplicate_counts.get(normalize(query), 0) > 1:
            issues.append("duplicate_query")
        if has_expected_scheme and not matching_indices:
            issues.append("scheme_identity_unverified")

        manual_review = bool(issues)
        rows.append({
            "query_number": position,
            "query": query,
            "expected_match": expected_match,
            "expected_scheme": expected_scheme,
            "label_class": "positive" if expected_match is True else "negative" if expected_match is False else "unknown",
            "expected_scheme_exists_in_dataset": bool(matching_indices),
            "matching_dataset_row_indices": ";".join(str(index) for index in matching_indices),
            "matching_scheme_names": "; ".join(str(dataset.iloc[index]["scheme_name"]) for index in matching_indices),
            "matching_scheme_slugs": "; ".join(str(dataset.iloc[index]["slug"]) for index in matching_indices),
            "exact_match_type": match_type,
            "possible_dataset_specific_matches": "; ".join(
                f"{dataset.iloc[index]['scheme_name']} [{dataset.iloc[index]['slug']}]"
                for index, _ in possible
            ),
            "duplicate_query_count": duplicate_counts.get(normalize(query), 0),
            "label_issues": ";".join(issues),
            "requires_manual_review": manual_review,
        })

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    parser.add_argument("--queries", type=Path, default=script_dir / "test_queries.json")
    parser.add_argument("--dataset", type=Path, default=root_dir / "dataset" / "govt_schemes.csv")
    parser.add_argument(
        "--output",
        type=Path,
        default=script_dir / "label_audit.csv",
    )
    args = parser.parse_args()

    audit = audit_labels(args.queries, args.dataset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    audit.to_csv(args.output, index=False)
    print(f"Audited {len(audit)} queries")
    print(f"Manual review required: {int(audit['requires_manual_review'].sum())}")
    print(f"Duplicate query rows: {int((audit['duplicate_query_count'] > 1).sum())}")
    print(f"Verified expected schemes: {int(audit['expected_scheme_exists_in_dataset'].sum())}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()