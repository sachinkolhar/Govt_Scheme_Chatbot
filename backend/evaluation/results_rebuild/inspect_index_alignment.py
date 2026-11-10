"""Read-only inspection of current FAISS/index-to-dataset alignment evidence."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

try:
    import faiss
except ImportError:
    faiss = None


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[2]
DATASET_PATH = ROOT_DIR / "dataset" / "govt_schemes.csv"
INDEX_PATH = ROOT_DIR / "model" / "scheme_index.faiss"
EMBEDDINGS_PATH = ROOT_DIR / "model" / "scheme_embeddings.npy"
SOURCE_ROOTS = [ROOT_DIR / "backend"]
SEARCH_PATTERNS = {
    "index_build": r"index\.add|write_index|IndexIDMap|IndexFlat",
    "embedding_generation": r"SentenceTransformer|\.encode\(",
    "ordering_operations": r"sort_values|drop_duplicates|sample\(|shuffle|reset_index",
    "positional_lookup": r"dataframe\.iloc|df\.iloc",
    "explicit_id_mapping": r"IndexIDMap|id_map|index_to|faiss_id|dataset_id",
}


def source_matches() -> dict[str, list[str]]:
    matches = {key: [] for key in SEARCH_PATTERNS}
    seen: set[Path] = set()
    paths = [path for root in SOURCE_ROOTS if root.exists() for path in root.rglob("*.py")]
    paths.extend(ROOT_DIR.glob("*.py"))
    for path in paths:
        if path in seen or "__pycache__" in path.parts:
            continue
        seen.add(path)
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        relative = path.relative_to(ROOT_DIR).as_posix()
        for line_number, line in enumerate(lines, start=1):
            for key, pattern in SEARCH_PATTERNS.items():
                if re.search(pattern, line):
                    matches[key].append(f"{relative}:{line_number}: {line.strip()}")
    return matches


def inspect_structural_alignment() -> dict[str, object]:
    """Load only the CSV and FAISS index and report structural facts."""
    dataset = pd.read_csv(DATASET_PATH)
    index = faiss.read_index(str(INDEX_PATH))
    dataset_rows = len(dataset)
    vector_count = int(index.ntotal)
    positional_ids = range(vector_count)
    invalid_ids = [
        vector_id
        for vector_id in positional_ids
        if vector_id < 0 or vector_id >= dataset_rows
    ]
    metric_names = {
        getattr(faiss, "METRIC_INNER_PRODUCT", -1): "METRIC_INNER_PRODUCT",
        getattr(faiss, "METRIC_L2", -1): "METRIC_L2",
    }
    return {
        "dataset_rows": dataset_rows,
        "vector_count": vector_count,
        "dimension": int(index.d),
        "metric_type": metric_names.get(index.metric_type, str(index.metric_type)),
        "positional_ids_in_dataframe_range": not invalid_ids,
        "invalid_positional_ids": invalid_ids,
        "scheme_embeddings_exists": EMBEDDINGS_PATH.is_file(),
    }


def main() -> int:
    print("Read-only FAISS alignment inspection")
    print(f"Dataset: {DATASET_PATH.relative_to(ROOT_DIR).as_posix()} exists={DATASET_PATH.exists()}")
    print(f"Index: {INDEX_PATH.relative_to(ROOT_DIR).as_posix()} exists={INDEX_PATH.exists()}")
    print(
        f"Saved embeddings: {EMBEDDINGS_PATH.relative_to(ROOT_DIR).as_posix()} "
        f"exists={EMBEDDINGS_PATH.is_file()}"
    )

    if faiss is None:
        print("FAISS inspection: Not verified because faiss is unavailable")
    elif not DATASET_PATH.is_file() or not INDEX_PATH.is_file():
        print("FAISS inspection: Not verified because the index is missing")
    else:
        facts = inspect_structural_alignment()
        print(f"Dataset rows: {facts['dataset_rows']}")
        print(f"Vector count: {facts['vector_count']}")
        print(f"Dimension: {facts['dimension']}")
        print(f"Metric type: {facts['metric_type']}")
        print(
            "All implicit positional FAISS IDs are in dataframe range: "
            f"{facts['positional_ids_in_dataframe_range']}"
        )
        if facts["invalid_positional_ids"]:
            print(f"Invalid positional IDs: {facts['invalid_positional_ids']}")

    matches = source_matches()
    for key, lines in matches.items():
        print(f"{key} matches: {len(lines)}")
        for line in lines:
            print(f"  {line}")

    print(
        "Alignment conclusion: Not verified. No build-time row-order proof or explicit "
        "FAISS-ID-to-dataset mapping was found; equal counts are insufficient."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
