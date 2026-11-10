"""Semantic search helpers for scheme retrieval."""
import math
import re
import threading
from collections import Counter
from typing import Any

import numpy as np
import pandas as pd

try:
    import faiss
except ImportError:
    faiss = None

try:
    from ..config.settings import BM25_ENABLED, CHAT_TOP_N, FAISS_MAX_DISTANCE, SEMANTIC_RETRIEVAL_TOP_K
    from ..models.schemas import SchemeResult
    from ..utils.text_processing import clean_text
except ImportError:
    from config.settings import BM25_ENABLED, CHAT_TOP_N, FAISS_MAX_DISTANCE, SEMANTIC_RETRIEVAL_TOP_K
    from models.schemas import SchemeResult
    from utils.text_processing import clean_text


encoder: Any = None
faiss_index: Any = None
df = pd.DataFrame()
FAISS_L2_METRIC = getattr(faiss, "METRIC_L2", 1)
_bm25_lock = threading.RLock()
_bm25_cache: tuple[int, int, list[Counter], dict[str, int], float] | None = None


def _tokens(value: Any) -> list[str]:
    return re.findall(r"[a-z0-9]+", str(value or "").lower())


def _get_bm25_index() -> tuple[list[Counter], dict[str, int], float]:
    """Build a small in-memory BM25 corpus once per dataframe instance."""
    global _bm25_cache
    with _bm25_lock:
        if _bm25_cache and _bm25_cache[:2] == (id(df), len(df)):
            return _bm25_cache[2:]
        columns = [column for column in (
            "scheme_name", "details", "benefits", "eligibility", "application",
            "documents", "tags", "schemeCategory", "level",
        ) if column in df.columns]
        documents = [Counter(_tokens(" ".join(str(row.get(col, "")) for col in columns))) for _, row in df.iterrows()]
        lengths = [sum(doc.values()) for doc in documents]
        average_length = sum(lengths) / len(lengths) if lengths else 0.0
        document_frequency: Counter = Counter()
        for document in documents:
            document_frequency.update(document.keys())
        _bm25_cache = (id(df), len(df), documents, dict(document_frequency), average_length)
        return documents, dict(document_frequency), average_length


def _bm25_candidates(query: str, limit: int) -> list[int]:
    documents, document_frequency, average_length = _get_bm25_index()
    terms = _tokens(query)
    total = len(documents)
    if not terms or not total:
        return []
    scored = []
    for index, document in enumerate(documents):
        length = sum(document.values())
        score = 0.0
        for term in terms:
            frequency = document.get(term, 0)
            if not frequency:
                continue
            inverse = math.log(1 + (total - document_frequency.get(term, 0) + 0.5) / (document_frequency.get(term, 0) + 0.5))
            denominator = frequency + 1.2 * (1 - 0.75 + 0.75 * length / max(average_length, 1))
            score += inverse * frequency * 2.2 / denominator
        if score > 0:
            scored.append((index, score))
    scored.sort(key=lambda item: item[1], reverse=True)
    return [index for index, _ in scored[:limit]]


def hybrid_candidates(query: str, top_k: int = CHAT_TOP_N) -> list[tuple[int, float]]:
    """Fuse FAISS and BM25 ranks while retaining authentic raw FAISS distances."""
    semantic = semantic_candidates(query, len(df) if BM25_ENABLED and not df.empty else top_k)
    if not BM25_ENABLED or not semantic:
        return semantic[:top_k]
    semantic_rank = {index: rank for rank, (index, _) in enumerate(semantic, start=1)}
    distances = dict(semantic)
    lexical = _bm25_candidates(query, top_k)
    lexical_rank = {index: rank for rank, index in enumerate(lexical, start=1)}
    # FAISS distances remain the eligibility cutoff and confidence signal. RRF
    # changes ordering only; BM25 never manufactures vector scores.
    fused = sorted(
        distances,
        key=lambda index: (
            (1 / (60 + semantic_rank[index])) + (1 / (60 + lexical_rank[index]) if index in lexical_rank else 0),
            -distances[index],
        ),
        reverse=True,
    )
    return [(index, distances[index]) for index in fused[:top_k]]


def configure_search_resources(
    semantic_encoder: Any,
    index: Any,
    dataframe: pd.DataFrame,
) -> None:
    """Register loaded model/index/dataframe resources for route helpers."""
    global encoder, faiss_index, df
    encoder = semantic_encoder
    faiss_index = index
    df = dataframe


def get_dataframe() -> pd.DataFrame:
    return df


def validate_search_resources(
    semantic_encoder: Any,
    index: Any,
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """Report FAISS compatibility facts without asserting row-order alignment."""
    metric_type = getattr(index, "metric_type", None)
    index_dimension = getattr(index, "d", None)
    vector_count = getattr(index, "ntotal", None)

    encoder_dimension = None
    dimension_method = getattr(semantic_encoder, "get_sentence_embedding_dimension", None)
    if callable(dimension_method):
        encoder_dimension = dimension_method()
    elif semantic_encoder is not None:
        encoder_dimension = getattr(semantic_encoder, "embedding_dimension", None)

    dimension_matches = None
    if index_dimension is not None and encoder_dimension is not None:
        dimension_matches = int(index_dimension) == int(encoder_dimension)

    dataset_count = len(dataframe) if dataframe is not None else None
    counts_equal = None
    if vector_count is not None and dataset_count is not None:
        counts_equal = int(vector_count) == dataset_count

    return {
        "metric_type": metric_type,
        "expected_metric_type": FAISS_L2_METRIC,
        "metric_is_l2": metric_type == FAISS_L2_METRIC,
        "index_dimension": index_dimension,
        "encoder_dimension": encoder_dimension,
        "dimension_matches": dimension_matches,
        "vector_count": vector_count,
        "vector_count_nonnegative": vector_count is not None and int(vector_count) >= 0,
        "dataset_count": dataset_count,
        "counts_equal": counts_equal,
        "row_alignment_verified": False,
    }


def is_faiss_distance_allowed(distance: float) -> bool:
    """Return whether a raw squared L2 distance passes the optional cutoff."""
    return FAISS_MAX_DISTANCE is None or distance <= FAISS_MAX_DISTANCE


def row_to_result(row: pd.Series, score: float = 0.0, match_score: int = 0, recommendation_reasons: list = None, is_favorite: bool = False) -> SchemeResult:
    if recommendation_reasons is None:
        recommendation_reasons = []
    return SchemeResult(
        scheme_name=str(row.get("scheme_name", "")),
        details=str(row.get("details", "")),
        benefits=str(row.get("benefits", "")),
        eligibility=str(row.get("eligibility", "")),
        application=str(row.get("application", "")),
        documents=str(row.get("documents", "")),
        level=str(row.get("level", "")),
        schemeCategory=str(row.get("schemeCategory", "")),
        tags=str(row.get("tags", "")),
        # Preserve the raw FAISS squared L2 distance; this is not confidence.
        score=float(score),
        match_score=int(match_score),
        recommendation_reasons=recommendation_reasons,
        is_favorite=is_favorite,
    )


def semantic_candidates(query: str, top_k: int = SEMANTIC_RETRIEVAL_TOP_K) -> list[tuple[int, float]]:
    if encoder is None or faiss_index is None or df.empty:
        return []

    cleaned = clean_text(query)
    embedding = encoder.encode([cleaned], convert_to_numpy=True).astype(np.float32)
    distances, indices = faiss_index.search(embedding, max(top_k, 1))

    best_by_index: dict[int, float] = {}
    for distance, idx in zip(distances[0], indices[0]):
        distance = float(distance)
        if not math.isfinite(distance) or not 0 <= idx < len(df):
            continue
        if is_faiss_distance_allowed(distance):
            row_index = int(idx)
            best_by_index[row_index] = min(distance, best_by_index.get(row_index, distance))
    out = list(best_by_index.items())
    out.sort(key=lambda candidate: candidate[1])
    return out


def get_db_relevant_schemes(query: str, limit: int = 5) -> list[SchemeResult]:
    max_needed = max(1, min(limit, 5))
    candidates = semantic_candidates(query, max(max_needed * 8, 20))
    out: list[SchemeResult] = []
    seen: set[int] = set()
    for idx, distance in candidates:
        if idx in seen:
            continue
        if not is_faiss_distance_allowed(distance):
            continue
        out.append(row_to_result(df.iloc[idx], distance))
        seen.add(idx)
        if len(out) >= max_needed:
            break
    return out
