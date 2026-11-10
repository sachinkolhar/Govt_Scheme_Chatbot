"""Corrected, non-destructive evaluation pipeline for an L2 FAISS index.

This script writes to a separate output directory by default. It does not
modify the existing evaluation pipeline or its generated results.
"""

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import faiss
import joblib
import numpy as np
import pandas as pd


DEFAULT_THRESHOLDS = (0.2, 0.3, 0.4, 0.5, 0.6)
AMBIGUITY_MARGIN = 0.05


@dataclass
class QueryResult:
    query: str
    expected_scheme: Optional[str]
    expected_match: bool
    matched_scheme: Optional[str]
    top_distance: float
    second_distance: float
    is_ambiguous: bool
    threshold: float
    is_accepted: bool
    is_correct: bool


def normalize_label(value: Any) -> str:
    """Normalize labels for deterministic exact comparisons."""
    return " ".join(str(value or "").casefold().split())


def load_and_validate_queries(path: Path, dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    queries = json.loads(path.read_text(encoding="utf-8"))
    scheme_names = {
        normalize_label(value): value
        for value in dataframe["scheme_name"].dropna()
        if normalize_label(value)
    }
    slugs = {
        normalize_label(value): value
        for value in dataframe["slug"].dropna()
        if normalize_label(value)
    }

    unmatched: list[tuple[int, str, str]] = []
    for position, query in enumerate(queries, start=1):
        expected_match = bool(query.get("expected_match", False))
        expected_scheme = query.get("expected_scheme")
        if expected_match and not expected_scheme:
            unmatched.append((position, query["query"], "missing expected_scheme"))
            continue
        if expected_match:
            label = normalize_label(expected_scheme)
            if label not in scheme_names and label not in slugs:
                unmatched.append((position, query["query"], str(expected_scheme)))

    if unmatched:
        details = "\n".join(
            f"  query {position}: {query!r} -> {label!r}"
            for position, query, label in unmatched
        )
        raise ValueError(
            "Positive labels do not resolve to an exact dataset scheme_name or "
            f"slug. Update the source labels or provide an approved mapping; do not "
            f"infer one automatically.\n{details}"
        )

    return queries


def resolve_expected_index(expected_scheme: Optional[str], dataframe: pd.DataFrame) -> Optional[int]:
    if not expected_scheme:
        return None
    expected = normalize_label(expected_scheme)
    for index, row in dataframe.iterrows():
        if expected in {normalize_label(row["scheme_name"]), normalize_label(row["slug"])}:
            return int(index)
    raise ValueError(f"Unresolved expected scheme: {expected_scheme}")


def semantic_search(query: str, encoder: Any, index: Any, dataframe: pd.DataFrame, top_k: int = 5) -> list[tuple[int, float]]:
    embedding = encoder.encode([query.lower().strip()], convert_to_numpy=True).astype(np.float32)
    distances, indices = index.search(embedding, min(top_k, index.ntotal))
    return [
        (int(candidate), float(distance))
        for distance, candidate in zip(distances[0], indices[0])
        if 0 <= candidate < len(dataframe)
    ]


def evaluate_query(query_data: dict[str, Any], results: list[tuple[int, float]], threshold: float, dataframe: pd.DataFrame) -> QueryResult:
    top_distance = results[0][1] if results else float("inf")
    second_distance = results[1][1] if len(results) > 1 else float("inf")
    matched_index = results[0][0] if results else None
    matched_scheme = dataframe.iloc[matched_index]["scheme_name"] if matched_index is not None else None
    is_ambiguous = bool(results) and (second_distance - top_distance < AMBIGUITY_MARGIN)
    is_accepted = bool(results) and top_distance <= threshold
    expected_match = bool(query_data.get("expected_match", False))
    expected_index = resolve_expected_index(query_data.get("expected_scheme"), dataframe)

    if expected_match:
        is_correct = is_accepted and matched_index == expected_index
    else:
        is_correct = not is_accepted

    return QueryResult(
        query=query_data["query"],
        expected_scheme=query_data.get("expected_scheme"),
        expected_match=expected_match,
        matched_scheme=matched_scheme,
        top_distance=top_distance,
        second_distance=second_distance,
        is_ambiguous=is_ambiguous,
        threshold=threshold,
        is_accepted=is_accepted,
        is_correct=is_correct,
    )


def calculate_metrics(results: list[QueryResult], threshold: float) -> dict[str, Any]:
    tp = fp = tn = fn = 0
    for result in results:
        if result.expected_match:
            if result.is_correct:
                tp += 1
            else:
                fn += 1
        elif result.is_correct:
            tn += 1
        else:
            fp += 1

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    total = len(results)
    return {
        "threshold": threshold,
        "accuracy": (tp + tn) / total if total else 0.0,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "ambiguous_matches": sum(result.is_ambiguous for result in results),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thresholds", nargs="+", type=float, default=DEFAULT_THRESHOLDS)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "results_corrected")
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    queries_path = script_dir / "test_queries.json"
    dataframe = pd.read_csv(root_dir / "dataset" / "govt_schemes.csv").fillna("")
    index = faiss.read_index(str(root_dir / "model" / "scheme_index.faiss"))
    if index.metric_type != faiss.METRIC_L2:
        raise ValueError(f"Expected an L2 index, found metric type {index.metric_type}")
    encoder = joblib.load(root_dir / "model" / "semantic_encoder.pkl")
    if hasattr(encoder, "to"):
        encoder.to("cpu")

    queries = load_and_validate_queries(queries_path, dataframe)
    all_results: list[QueryResult] = []
    metrics: list[dict[str, Any]] = []
    for threshold in args.thresholds:
        query_results = [
            evaluate_query(query, semantic_search(query["query"], encoder, index, dataframe), threshold, dataframe)
            for query in queries
        ]
        all_results.extend(query_results)
        metrics.append(calculate_metrics(query_results, threshold))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(metrics).to_csv(args.output_dir / "evaluation_summary.csv", index=False)
    pd.DataFrame([
        {
            "query": result.query,
            "expected_scheme": result.expected_scheme,
            "matched_scheme": result.matched_scheme,
            "top_distance": result.top_distance,
            "second_distance": result.second_distance,
            "threshold": result.threshold,
            "accepted": result.is_accepted,
            "ambiguous": result.is_ambiguous,
            "correct": result.is_correct,
        }
        for result in all_results
    ]).to_csv(args.output_dir / "evaluation_results_detailed.csv", index=False)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()