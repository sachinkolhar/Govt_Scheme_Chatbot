"""Standalone cosine-similarity retrieval over the Colab scheme chunks.

This module is deliberately separate from backend.search.semantic, whose
production FAISS index uses squared L2 distances over scheme-level rows.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "chunk_id",
    "scheme_id",
    "scheme_name",
    "field_type",
    "chunk_text",
    "level",
}


class ChunkRetriever:
    """Retrieve and group chunk-level matches without changing production search."""

    def __init__(
        self,
        chunks: pd.DataFrame,
        index: Any,
        encoder: Any,
    ) -> None:
        missing = REQUIRED_COLUMNS.difference(chunks.columns)
        if missing:
            raise ValueError(f"Chunk metadata is missing columns: {sorted(missing)}")

        self.chunks = chunks.reset_index(drop=True).copy()
        self.index = index
        self.encoder = encoder

        if self.chunks.empty:
            raise ValueError("Chunk metadata is empty")

        chunk_ids = pd.to_numeric(self.chunks["chunk_id"], errors="coerce")
        if chunk_ids.isna().any() or not chunk_ids.is_unique:
            raise ValueError("chunk_id values must be numeric and unique")

        if not np.array_equal(
            chunk_ids.to_numpy(dtype=np.int64),
            np.arange(len(self.chunks), dtype=np.int64),
        ):
            raise ValueError(
                "Chunk rows must be ordered by contiguous chunk_id starting at zero"
            )

        index_count = int(getattr(index, "ntotal", -1))
        index_dimension = int(getattr(index, "d", -1))
        if index_count != len(self.chunks):
            raise ValueError(
                f"Index contains {index_count} vectors but metadata has "
                f"{len(self.chunks)} rows"
            )

        encoder_dimension = encoder.get_sentence_embedding_dimension()
        if index_dimension != int(encoder_dimension):
            raise ValueError(
                f"Encoder dimension {encoder_dimension} does not match "
                f"index dimension {index_dimension}"
            )

        # The artifact index is expected to use inner product over normalized vectors.
        metric_type = getattr(index, "metric_type", None)
        try:
            import faiss
        except ImportError as exc:
            raise RuntimeError("faiss is required to validate the chunk index") from exc

        if metric_type != faiss.METRIC_INNER_PRODUCT:
            raise ValueError(
                "Chunk index must use inner product; normalized vectors then "
                "produce cosine similarity"
            )

    @classmethod
    def from_files(
        cls,
        chunks_path: str | Path,
        index_path: str | Path,
        encoder_name_path: str | Path,
    ) -> "ChunkRetriever":
        """Load the saved metadata, FAISS index, and its declared encoder."""
        try:
            import faiss
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "faiss-cpu and sentence-transformers are required for chunk retrieval"
            ) from exc

        chunks_path = Path(chunks_path)
        index_path = Path(index_path)
        encoder_name_path = Path(encoder_name_path)

        for path in (chunks_path, index_path, encoder_name_path):
            if not path.is_file():
                raise FileNotFoundError(f"Required chunk artifact not found: {path}")

        encoder_name = encoder_name_path.read_text(encoding="utf-8").strip()
        if not encoder_name:
            raise ValueError("Encoder name file is empty")

        chunks = pd.read_csv(chunks_path).fillna("")
        index = faiss.read_index(str(index_path))
        encoder = SentenceTransformer(encoder_name)

        return cls(chunks, index, encoder)

    def retrieve(
        self,
        query: str,
        top_k_chunks: int = 50,
        top_k_schemes: int = 5,
        level: str | None = None,
        category: str | None = None,
        field_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return best matching chunks grouped by scheme, highest score first."""
        if not isinstance(query, str) or not query.strip():
            return []
        if top_k_chunks < 1 or top_k_schemes < 1:
            return []

        query_vector = self.encoder.encode(
            [query.strip()],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        query_vector = np.asarray(query_vector, dtype=np.float32)

        if query_vector.shape != (1, int(self.index.d)):
            raise ValueError(
                f"Unexpected query embedding shape: {query_vector.shape}"
            )
        if not np.isfinite(query_vector).all():
            raise ValueError("Query embedding contains non-finite values")

        norm = float(np.linalg.norm(query_vector[0]))
        if not np.isclose(norm, 1.0, atol=1e-4):
            raise ValueError("Query embedding is not normalized")

        search_k = min(int(top_k_chunks), int(self.index.ntotal))
        similarities, indices = self.index.search(query_vector, search_k)

        candidates: list[dict[str, Any]] = []
        for similarity, row_index in zip(similarities[0], indices[0]):
            row_index = int(row_index)
            if row_index < 0 or row_index >= len(self.chunks):
                continue

            score = float(similarity)
            if not np.isfinite(score):
                continue

            row = self.chunks.iloc[row_index]
            if level and str(row["level"]).casefold() != level.casefold():
                continue

            if category:
                category_values = row.get("category_list_parsed", "")
                category_text = (
                    " ".join(category_values)
                    if isinstance(category_values, list)
                    else str(category_values)
                )
                category_text += " " + str(row.get("normalized_categories", ""))
                if category.casefold() not in category_text.casefold():
                    continue

            if field_type and str(row["field_type"]).casefold() != field_type.casefold():
                continue

            candidates.append({
                "chunk_id": int(row["chunk_id"]),
                "scheme_id": str(row["scheme_id"]),
                "scheme_name": str(row["scheme_name"]),
                "field_type": str(row["field_type"]),
                "chunk_text": str(row["chunk_text"]),
                "level": str(row["level"]),
                "similarity": score,
            })

        # Keep each scheme's strongest chunk, with deterministic tie handling.
        best_by_scheme: dict[str, dict[str, Any]] = {}
        for candidate in candidates:
            scheme_id = candidate["scheme_id"]
            previous = best_by_scheme.get(scheme_id)
            if previous is None or candidate["similarity"] > previous["similarity"]:
                best_by_scheme[scheme_id] = candidate

        results = sorted(
            best_by_scheme.values(),
            key=lambda item: (-item["similarity"], item["scheme_id"]),
        )
        return results[: int(top_k_schemes)]
