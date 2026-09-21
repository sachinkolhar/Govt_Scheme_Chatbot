"""Semantic search helpers for scheme retrieval."""
from typing import Any

import numpy as np
import pandas as pd

try:
    from ..config.settings import FAISS_MIN_SCORE
    from ..models.schemas import SchemeResult
    from ..utils.text_processing import clean_text
except ImportError:
    from config.settings import FAISS_MIN_SCORE
    from models.schemas import SchemeResult
    from utils.text_processing import clean_text


encoder: Any = None
faiss_index: Any = None
df = pd.DataFrame()


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
        score=float(score),
        match_score=int(match_score),
        recommendation_reasons=recommendation_reasons,
        is_favorite=is_favorite,
    )


def semantic_candidates(query: str, top_k: int) -> list[tuple[int, float]]:
    if encoder is None or faiss_index is None or df.empty:
        return []

    cleaned = clean_text(query)
    embedding = encoder.encode([cleaned], convert_to_numpy=True).astype(np.float32)
    distances, indices = faiss_index.search(embedding, max(top_k, 1))

    out: list[tuple[int, float]] = []
    for score, idx in zip(distances[0], indices[0]):
        if 0 <= idx < len(df):
            out.append((int(idx), float(score)))
    return out


def get_db_relevant_schemes(query: str, limit: int = 5) -> list[SchemeResult]:
    max_needed = max(1, min(limit, 5))
    candidates = semantic_candidates(query, max(max_needed * 8, 20))
    out: list[SchemeResult] = []
    seen: set[int] = set()
    for idx, score in candidates:
        if idx in seen:
            continue
        if score < FAISS_MIN_SCORE:
            continue
        out.append(row_to_result(df.iloc[idx], score))
        seen.add(idx)
        if len(out) >= max_needed:
            break
    return out
