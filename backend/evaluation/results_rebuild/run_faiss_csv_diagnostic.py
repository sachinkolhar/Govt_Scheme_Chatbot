"""Run a read-only probe of production FAISS IDs against the production CSV."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import torch

try:
    import faiss
except ImportError as exc:
    raise SystemExit("FAISS is required; run this with the repository virtual environment.") from exc


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[2]
PRODUCTION_CSV = ROOT_DIR / "dataset" / "govt_schemes.csv"
BUILD_INPUT_CSV = ROOT_DIR / "dataset.csv"
INDEX_PATH = ROOT_DIR / "model" / "scheme_index.faiss"
ENCODER_PATH = ROOT_DIR / "model" / "semantic_encoder.pkl"
SAVED_EMBEDDINGS_PATH = ROOT_DIR / "model" / "scheme_embeddings.npy"
RESULTS_PATH = SCRIPT_DIR / "faiss_csv_diagnostic_results.csv"
SUMMARY_PATH = SCRIPT_DIR / "faiss_csv_diagnostic_summary.json"
SAMPLE_SIZE = 12
TOP_K = 5


def load_production_resources() -> tuple[Any, Any, pd.DataFrame]:
    """Load the same three resources and CSV null handling as backend.main."""
    original_torch_load = torch.load

    def cpu_torch_load(*args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("map_location", "cpu")
        kwargs.setdefault("weights_only", False)
        return original_torch_load(*args, **kwargs)

    torch.load = cpu_torch_load
    try:
        encoder = joblib.load(ENCODER_PATH)
    finally:
        torch.load = original_torch_load
    index = faiss.read_index(str(INDEX_PATH))
    dataframe = pd.read_csv(PRODUCTION_CSV).fillna("")
    return encoder, index, dataframe


def select_known_schemes(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Select deterministic, non-empty records spread across the CSV."""
    candidates = dataframe[
        dataframe["scheme_name"].astype(str).str.strip().ne("")
        & dataframe["details"].astype(str).str.strip().ne("")
    ].copy()
    if len(candidates) < SAMPLE_SIZE:
        raise RuntimeError(f"Only {len(candidates)} usable scheme descriptions were found.")
    positions = np.linspace(0, len(candidates) - 1, SAMPLE_SIZE, dtype=int)
    return candidates.iloc[positions]


def compare_source_row_order(dataframe: pd.DataFrame) -> dict[str, Any]:
    """Compare the current production CSV to the notebook's build-input CSV."""
    result: dict[str, Any] = {
        "status": "NOT_CHECKED",
        "build_input_exists": BUILD_INPUT_CSV.is_file(),
        "row_count_equal": None,
        "identity_columns_equal_in_order": None,
        "note": (
            "The production app loads dataset/govt_schemes.csv; the notebook build "
            "loads root dataset.csv."
        ),
    }
    if not BUILD_INPUT_CSV.is_file():
        result["status"] = "UNAVAILABLE"
        result["note"] += " The notebook input file is missing."
        return result

    build_input = pd.read_csv(BUILD_INPUT_CSV).fillna("")
    result["row_count_equal"] = len(build_input) == len(dataframe)
    identity_columns = ["scheme_name", "slug", "details", "benefits", "eligibility"]
    missing = [column for column in identity_columns if column not in build_input or column not in dataframe]
    if missing:
        result["status"] = "UNAVAILABLE"
        result["note"] += f" Missing identity columns: {missing}."
        return result

    result["identity_columns_equal_in_order"] = build_input[identity_columns].reset_index(
        drop=True
    ).equals(dataframe[identity_columns].reset_index(drop=True))
    result["status"] = (
        "PASSED"
        if result["row_count_equal"] and result["identity_columns_equal_in_order"]
        else "FAILED"
    )
    return result


def inspect_index_source_order() -> dict[str, Any]:
    """Record source-level evidence without treating it as runtime proof."""
    notebook_text = (ROOT_DIR / "mini.ipynb").read_text(encoding="utf-8")
    rebuild_text = (
        ROOT_DIR / "backend" / "evaluation" / "results_rebuild" /
        "rebuild_notebook_artifacts.py"
    ).read_text(encoding="utf-8")
    notebook_has_build_sequence = all(
        needle in notebook_text
        for needle in (
            "sbert_model.encode",
            "cleaned_text",
            "IndexFlatL2",
            "index.add(scheme_embeddings)",
        )
    )
    rebuild_has_build_sequence = all(
        needle in rebuild_text
        for needle in (
            "df = pandas.read_csv(INPUT_DATASET)",
            'df.drop(columns=["Unnamed: 9"], inplace=True)',
            "sbert_model.encode(",
            "index = faiss.IndexFlatL2(",
            "index.add(embeddings)",
        )
    )
    return {
        "status": "PASSED" if notebook_has_build_sequence and rebuild_has_build_sequence else "FAILED",
        "notebook_evidence": [
            "mini.ipynb encodes df['cleaned_text'] in dataframe order.",
            "mini.ipynb creates IndexFlatL2 and calls index.add(scheme_embeddings).",
        ],
        "rebuild_evidence": (
            "rebuild_notebook_artifacts.py reads dataset.csv, drops only Unnamed: 9, "
            "does not reorder rows, and encodes processed rows in order."
            if all(
                needle in rebuild_text
                for needle in (
                    "df = pandas.read_csv(INPUT_DATASET)",
                    'df.drop(columns=["Unnamed: 9"], inplace=True)',
                    'sbert_model.encode(',
                    'index = faiss.IndexFlatL2(',
                    "index.add(embeddings)",
                )
            )
            else "Expected rebuild source statements were not all found."
        ),
    }


def run_diagnostic(encoder: Any, index: Any, dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    """Search actual descriptions and map every returned ID with dataframe.iloc."""
    try:
        from backend.utils.text_processing import clean_text
    except ImportError as exc:
        raise RuntimeError("Could not import the production query cleaner.") from exc

    rows: list[dict[str, Any]] = []
    for query_row in select_known_schemes(dataframe).itertuples():
        query_name = str(query_row.scheme_name)
        query_description = str(query_row.details)
        cleaned_query = clean_text(query_description)
        query_vector = encoder.encode([cleaned_query], convert_to_numpy=True).astype(np.float32)
        distances, indices = index.search(query_vector, min(TOP_K, int(index.ntotal)))
        for rank, (distance, vector_id) in enumerate(zip(distances[0], indices[0]), start=1):
            vector_id = int(vector_id)
            valid_id = 0 <= vector_id < len(dataframe)
            retrieved_name = str(dataframe.iloc[vector_id]["scheme_name"]) if valid_id else ""
            rows.append(
                {
                    "query_scheme_name": query_name,
                    "query_description": query_description,
                    "query_csv_row_index": int(query_row.Index),
                    "faiss_rank": rank,
                    "faiss_vector_id": vector_id,
                    "squared_l2_distance": float(distance),
                    "retrieved_csv_row_index": vector_id if valid_id else "",
                    "retrieved_csv_scheme_name": retrieved_name,
                    "expected_and_retrieved_name_match": valid_id and retrieved_name == query_name,
                }
            )
    return rows


def reconstruct_check(rows: list[dict[str, Any]], index: Any) -> dict[str, Any]:
    """Compare selected index vectors with the production saved embedding file."""
    if not SAVED_EMBEDDINGS_PATH.is_file():
        return {
            "status": "UNAVAILABLE",
            "path": str(SAVED_EMBEDDINGS_PATH.relative_to(ROOT_DIR)),
            "message": "Production saved embedding file is missing; reconstruct comparison was not possible.",
        }

    saved = np.load(SAVED_EMBEDDINGS_PATH, allow_pickle=False)
    ids = sorted({int(row["faiss_vector_id"]) for row in rows if int(row["faiss_vector_id"]) >= 0})
    checks = []
    for vector_id in ids:
        if vector_id >= len(saved):
            checks.append({"vector_id": vector_id, "allclose": False, "reason": "ID outside saved embedding rows"})
            continue
        reconstructed = np.asarray(index.reconstruct(vector_id), dtype=np.float32)
        checks.append({
            "vector_id": vector_id,
            "allclose": bool(np.allclose(reconstructed, saved[vector_id])),
            "max_abs_difference": float(np.max(np.abs(reconstructed - saved[vector_id]))),
        })
    return {
        "status": "PASSED" if checks and all(item["allclose"] for item in checks) else "FAILED",
        "path": str(SAVED_EMBEDDINGS_PATH.relative_to(ROOT_DIR)),
        "checked_vectors": len(checks),
        "checks": checks,
    }


def main() -> int:
    if not all(path.is_file() for path in (PRODUCTION_CSV, INDEX_PATH, ENCODER_PATH)):
        missing = [str(path.relative_to(ROOT_DIR)) for path in (PRODUCTION_CSV, INDEX_PATH, ENCODER_PATH) if not path.is_file()]
        raise SystemExit(f"Missing production artifacts: {missing}")

    encoder, index, dataframe = load_production_resources()
    rows = run_diagnostic(encoder, index, dataframe)
    source_order = compare_source_row_order(dataframe)
    build_order = inspect_index_source_order()
    reconstruction = reconstruct_check(rows, index)
    structural = {
        "csv_rows": len(dataframe),
        "faiss_vectors": int(index.ntotal),
        "counts_equal": int(index.ntotal) == len(dataframe),
        "index_dimension": int(index.d),
        "encoder_dimension": int(encoder.get_sentence_embedding_dimension()),
        "metric_type": "METRIC_L2" if index.metric_type == faiss.METRIC_L2 else str(index.metric_type),
        "all_returned_ids_in_csv_range": all(
            0 <= int(row["faiss_vector_id"]) < len(dataframe) for row in rows
        ),
    }

    with RESULTS_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "results_csv": str(RESULTS_PATH.relative_to(ROOT_DIR)),
        "source_files_and_functions": {
            "production_loader": "backend/main.py module initialization",
            "production_search": "backend/search/semantic.py:semantic_candidates",
            "production_mapping": "backend/search/semantic.py:get_db_relevant_schemes uses df.iloc[idx]",
            "query_cleaner": "backend/utils/text_processing.py:clean_text",
            "index_build": "mini.ipynb embedding/index cells; backend/evaluation/results_rebuild/rebuild_notebook_artifacts.py",
        },
        "structural_checks": structural,
        "source_row_order_check": source_order,
        "index_build_source_check": build_order,
        "reconstructed_vector_check": reconstruction,
        "query_checks": {
            "queries": len({row["query_scheme_name"] for row in rows}),
            "returned_rows": len(rows),
            "top1_matches": sum(
                row["faiss_rank"] == 1 and row["expected_and_retrieved_name_match"] for row in rows
            ),
            "top1_match_rate": sum(
                row["faiss_rank"] == 1 and row["expected_and_retrieved_name_match"] for row in rows
            ) / max(1, len({row["query_scheme_name"] for row in rows})),
        },
        "verdict": (
            "VERIFIED"
            if source_order["status"] == "PASSED"
            and reconstruction["status"] == "PASSED"
            and all(row["expected_and_retrieved_name_match"] for row in rows if row["faiss_rank"] == 1)
            else "PARTIALLY VERIFIED"
            if source_order["status"] == "PASSED"
            or any(row["expected_and_retrieved_name_match"] for row in rows if row["faiss_rank"] == 1)
            else "NOT VERIFIED"
        ),
        "interpretation": (
            "Query matches are semantic retrieval evidence, not proof that all FAISS IDs "
            "are aligned. Positional alignment is supported only by the independent source-order "
            "comparison and, when available, exact reconstructed-vector comparison."
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"\nDiagnostic CSV: {RESULTS_PATH}")
    print(f"Diagnostic summary: {SUMMARY_PATH}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT_DIR))
    raise SystemExit(main())
