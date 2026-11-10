"""Shared intent, fact, retrieval, eligibility, ranking and confidence pipeline."""
from dataclasses import dataclass, field
import math
from typing import Any, Mapping, Optional

import pandas as pd

try:
    from ..config.settings import CHAT_FINAL_K, FAISS_MAX_DISTANCE, SEMANTIC_RETRIEVAL_TOP_K
    from ..search.semantic import get_dataframe, semantic_candidates
    from ..search.ranking import RankedScheme, rank_candidates, _CATEGORY_SCORE
    from ..search.candidate_selection import scheme_identity, select_final_candidates
    from .facts import extract_user_facts
    from .intent import IntentResult, detect_intent
    from .clarification import confidence_band
except ImportError:
    from config.settings import CHAT_FINAL_K, FAISS_MAX_DISTANCE, SEMANTIC_RETRIEVAL_TOP_K
    from search.semantic import get_dataframe, semantic_candidates
    from search.ranking import RankedScheme, rank_candidates, _CATEGORY_SCORE
    from search.candidate_selection import scheme_identity, select_final_candidates
    from chat.facts import extract_user_facts
    from chat.intent import IntentResult, detect_intent
    from chat.clarification import confidence_band


@dataclass
class CandidateResolution:
    query: str
    intent: IntentResult
    facts: dict[str, Any]
    candidates: list[RankedScheme] = field(default_factory=list)
    confidence: str = "LOW_CONFIDENCE"
    confidence_score: float = 0.0
    missing_information: list[str] = field(default_factory=list)


def resolve_scheme_candidates(
    query: str,
    profile: Optional[Mapping[str, Any]] = None,
    intent: Optional[IntentResult] = None,
    scheme_names: Optional[list[str]] = None,
    top_k: Optional[int] = None,
    candidate_indices: Optional[list[tuple[int, float]]] = None,
    dataframe: Optional[pd.DataFrame] = None,
) -> CandidateResolution:
    """Adapt public FAISS ``(row_index, L2 distance)`` results to ranked rows."""
    dataframe = get_dataframe() if dataframe is None else dataframe
    if scheme_names is None:
        scheme_names = [str(name) for name in dataframe["scheme_name"].tolist()] if "scheme_name" in dataframe else []
    detected = intent or detect_intent(query, scheme_names)
    facts = extract_user_facts(query)
    merged_profile = {key: value for key, value in facts.items() if not key.startswith("_")}
    merged_profile.update({key: value for key, value in dict(profile or {}).items() if value is not None})
    k = max(1, int(top_k or SEMANTIC_RETRIEVAL_TOP_K))
    raw_candidates = candidate_indices if candidate_indices is not None else semantic_candidates(query, k)

    # FAISS's public contract remains (index, squared L2 distance); ranking gets rows.
    row_candidates: list[tuple[pd.Series, float]] = []
    for index, distance in raw_candidates:
        try:
            row_index = int(index)
            l2_distance = float(distance)
        except (TypeError, ValueError, OverflowError):
            continue
        if not math.isfinite(l2_distance) or l2_distance < 0:
            continue
        if FAISS_MAX_DISTANCE is not None and l2_distance > FAISS_MAX_DISTANCE:
            continue
        if 0 <= row_index < len(dataframe):
            row_candidates.append((dataframe.iloc[row_index], l2_distance))
    # Keep the strongest vector hit for each stable scheme identity before
    # ranking. Duplicate source rows must not occupy the final answer slots.
    best_by_identity = {}
    for row, distance in row_candidates:
        identity = scheme_identity(row)
        if identity not in best_by_identity or distance < best_by_identity[identity][1]:
            best_by_identity[identity] = (row, distance)
    ranked_pool = rank_candidates(
        list(best_by_identity.values()),
        profile=merged_profile,
        query=query,
        scheme_names=scheme_names,
        intent=detected.intent,
        target_group=detected.target_group,
        limit=1 if detected.scheme_name else CHAT_FINAL_K,
    )
    ranked = select_final_candidates(ranked_pool, detected.target_group, CHAT_FINAL_K)
    # Category is part of confidence: an unknown or mismatched beneficiary group
    # cannot become a confident answer solely through vector similarity.
    semantic_confidence = (1.0 / (1.0 + max(0.0, ranked[0].semantic_score))) if ranked else 0.0
    if ranked and detected.target_group:
        score = semantic_confidence * _CATEGORY_SCORE[ranked[0].category_relevance]
    else:
        score = semantic_confidence
    band = confidence_band(score)
    missing: list[str] = []
    for candidate in ranked:
        for field in candidate.missing_information:
            if field not in missing:
                missing.append(field)
    return CandidateResolution(query, detected, merged_profile, ranked, band, score, missing)
