"""Diagnose top-k score distributions for the current FAISS evaluation.

This script does not modify the original evaluation pipeline or its results.
It evaluates binary acceptance using only the existing ``expected_match``
labels; it does not claim that the retrieved scheme is the expected scheme.
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any

import faiss
import joblib
import numpy as np
import pandas as pd

try:
    import torch
except ImportError:
    torch = None


DEFAULT_THRESHOLDS = (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.5)


def setup_cpu_loading() -> None:
    if torch is None:
        return
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    torch.cuda.is_available = lambda: False  # type: ignore
    original_load = torch.load

    def load_on_cpu(*args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("map_location", torch.device("cpu"))
        kwargs.setdefault("weights_only", False)
        return original_load(*args, **kwargs)

    torch.load = load_on_cpu  # type: ignore


def describe(values: pd.Series) -> dict[str, float | int]:
    summary = values.describe(percentiles=[0.25, 0.5, 0.75])
    return {
        "count": int(summary["count"]),
        "min": float(summary["min"]),
        "25%": float(summary["25%"]),
        "median": float(summary["50%"]),
        "mean": float(summary["mean"]),
        "75%": float(summary["75%"]),
        "max": float(summary["max"]),
        "std": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
    }


def calculate_metrics(scores: pd.DataFrame, threshold: float) -> dict[str, float | int]:
    accepted = scores["top_distance"] <= threshold
    expected_positive = scores["expected_match"]
    tp = int((accepted & expected_positive).sum())
    fp = int((accepted & ~expected_positive).sum())
    tn = int((~accepted & ~expected_positive).sum())
    fn = int((~accepted & expected_positive).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "threshold": threshold,
        "accuracy": (tp + tn) / len(scores) if len(scores) else 0.0,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thresholds", nargs="+", type=float, default=DEFAULT_THRESHOLDS)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "score_diagnostic_results",
    )
    args = parser.parse_args()

    setup_cpu_loading()
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent.parent
    queries = json.loads((script_dir / "test_queries.json").read_text(encoding="utf-8"))
    dataframe = pd.read_csv(root_dir / "dataset" / "govt_schemes.csv").fillna("")
    index = faiss.read_index(str(root_dir / "model" / "scheme_index.faiss"))
    if index.metric_type != faiss.METRIC_L2:
        raise ValueError(f"Expected METRIC_L2, found metric type {index.metric_type}")

    encoder = joblib.load(root_dir / "model" / "semantic_encoder.pkl")
    if hasattr(encoder, "to"):
        encoder.to("cpu")

    records: list[dict[str, Any]] = []
    for query_number, query_data in enumerate(queries, start=1):
        embedding = encoder.encode(
            [query_data["query"].lower().strip()],
            convert_to_numpy=True,
        ).astype(np.float32)
        distances, indices = index.search(embedding, 2)
        top_index = int(indices[0][0])
        records.append(
            {
                "query_number": query_number,
                "query": query_data["query"],
                "expected_scheme": query_data.get("expected_scheme"),
                "expected_match": bool(query_data.get("expected_match", False)),
                "matched_scheme": dataframe.iloc[top_index]["scheme_name"] if top_index >= 0 else None,
                "top_distance": float(distances[0][0]) if top_index >= 0 else float("inf"),
                "second_distance": float(distances[0][1]) if indices[0][1] >= 0 else float("inf"),
            }
        )

    scores = pd.DataFrame(records)
    stats = pd.DataFrame(
        [
            {"label": "positive", **describe(scores.loc[scores["expected_match"], "top_distance"])},
            {"label": "negative", **describe(scores.loc[~scores["expected_match"], "top_distance"])},
            {"label": "all", **describe(scores["top_distance"])},
        ]
    )
    threshold_table = pd.DataFrame(calculate_metrics(scores, threshold) for threshold in args.thresholds)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    scores.to_csv(args.output_dir / "score_distribution_by_query.csv", index=False)
    stats.to_csv(args.output_dir / "score_distribution_statistics.csv", index=False)
    threshold_table.to_csv(args.output_dir / "threshold_comparison.csv", index=False)

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 6))
        positive = scores.loc[scores["expected_match"], "top_distance"]
        negative = scores.loc[~scores["expected_match"], "top_distance"]
        bins = max(8, min(30, len(scores) // 3))
        plt.hist(positive, bins=bins, alpha=0.65, label="expected_match=true")
        plt.hist(negative, bins=bins, alpha=0.65, label="expected_match=false")
        for threshold in args.thresholds:
            plt.axvline(threshold, linestyle="--", linewidth=0.8, alpha=0.5)
        plt.xlabel("Top squared L2 distance; lower is better")
        plt.ylabel("Query count")
        plt.title("FAISS top-distance distribution")
        plt.legend()
        plt.tight_layout()
        plt.savefig(args.output_dir / "score_distribution_histogram.png", dpi=150)
        plt.close()
    except ImportError:
        print("matplotlib is unavailable; skipped histogram generation")

    print(f"FAISS metric: METRIC_L2 (FAISS returns squared L2 distances)")
    print(f"Queries: {len(scores)}; positives: {int(scores['expected_match'].sum())}; negatives: {int((~scores['expected_match']).sum())}")
    print("\nDistance statistics:")
    print(stats.to_string(index=False))
    print("\nThreshold comparison:")
    print(threshold_table.to_string(index=False))
    print(f"\nWrote diagnostics to {args.output_dir}")
    print("These metrics measure binary acceptance only, not exact scheme retrieval correctness.")


if __name__ == "__main__":
    main()