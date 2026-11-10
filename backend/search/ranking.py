"""Rerank retrieved rows using the project's existing eligibility checker."""
from dataclasses import asdict, dataclass, field
import re
from typing import Any, Mapping, Optional, Sequence

try:
    from ..config.settings import RERANKER_ENABLED, RANK_WEIGHT_CATEGORY, RANK_WEIGHT_ELIGIBILITY, RANK_WEIGHT_INTENT, RANK_WEIGHT_SEMANTIC
    from ..models.schemas import EligibilityRequest
    from ..eligibility.checker import (
        calculate_match_score,
        is_eligible,
        is_state_compatible_before_scoring,
    )
    from .geography import geographic_classification
except ImportError:
    from config.settings import RERANKER_ENABLED, RANK_WEIGHT_CATEGORY, RANK_WEIGHT_ELIGIBILITY, RANK_WEIGHT_INTENT, RANK_WEIGHT_SEMANTIC
    from models.schemas import EligibilityRequest
    from eligibility.checker import calculate_match_score, is_eligible, is_state_compatible_before_scoring
    from search.geography import geographic_classification


@dataclass
class RankedScheme:
    scheme: Any
    # This field retains the raw squared L2 distance for API/debug traceability.
    semantic_score: float
    eligibility_score: float
    final_score: float
    eligibility_status: str
    matched_conditions: list[str] = field(default_factory=list)
    missing_information: list[str] = field(default_factory=list)
    category_relevance: str = "UNKNOWN"
    geography: str = "UNKNOWN"

    def to_dict(self) -> dict:
        return asdict(self)


def _as_eligibility_request(profile: Optional[Mapping[str, Any]]) -> EligibilityRequest:
    data = dict(profile or {})
    allowed = {
        "age", "gender", "state", "occupation", "income", "category",
        "disability", "student_status", "farmer_status",
    }
    return EligibilityRequest(**{key: data[key] for key in allowed if key in data})


def _missing_profile_fields(row: Any, profile: Mapping[str, Any]) -> list[str]:
    text = str(row.get("eligibility", "")).lower()
    markers = {
        "age": ("age", "years old", "year of age"),
        "income": ("income", "annual earnings"),
        "state": ("state", "resident", "domicile"),
        "category": ("caste", "category", "scheduled caste", "scheduled tribe", "obc"),
        "occupation": ("occupation", "farmer", "student", "worker", "employment"),
    }
    missing = []
    for field, terms in markers.items():
        supplied = field in profile
        if field == "occupation":
            supplied = supplied or bool(profile.get("student_status")) or bool(profile.get("farmer_status"))
        if not supplied and any(term in text for term in terms):
            missing.append(field)
    return missing


def _row_text(row: Any, fields: Sequence[str]) -> str:
    return " ".join(str(row.get(field, "") or "") for field in fields).casefold()


def category_relevance(row: Any, target_group: Optional[str]) -> str:
    """Classify evidence for a requested beneficiary group using source fields.

    Tags can signal a group, but do not override an explicit narrow occupation in
    the scheme's name, purpose, or eligibility text.
    """
    if not target_group:
        return "UNKNOWN"
    fields = ("scheme_name", "details", "eligibility", "benefits", "schemeCategory", "tags")
    blob = _row_text(row, fields)
    core = _row_text(row, ("scheme_name", "details", "eligibility", "benefits"))
    tags = _row_text(row, ("tags", "schemeCategory"))
    patterns = {
        "senior_citizen": r"\b(senior\s+citizens?|old[- ]age|elderly|old\s+persons?|vridh\w*|vriddh\w*|briddh\w*|aged\s+(?:persons?|citizens?))\b",
        "construction_worker": r"\b(construction\s+workers?|building\s+workers?|bocw)\b",
        "law_graduate": r"\b(law\s+graduates?|lawyers?)\b",
        "farmer": r"\b(farmers?|kisans?|krishak)\b",
        "student": r"\b(students?|scholarships?)\b",
        "women": r"\b(women|woman|widow|girl child)\b",
        "disability": r"\b(persons? with disabilit\w*|disabled|divyang|pwd|disability)\b",
        "worker": r"\b(workers?|labou?rer?s?|unorganised workers?)\b",
    }
    pattern = patterns.get(target_group)
    if not pattern:
        return "UNKNOWN"
    in_core = bool(re.search(pattern, core))
    in_metadata = bool(re.search(pattern, tags))
    if target_group == "senior_citizen":
        pension_context = bool(re.search(r"\b(pension|old[- ]age|retirement)\b", blob))
        other_group_patterns = [value for key, value in patterns.items() if key != "senior_citizen"]
        explicitly_other_group = any(re.search(value, core) for value in other_group_patterns)
        if explicitly_other_group and not re.search(pattern, core):
            return "NO_MATCH"
        if in_core and pension_context:
            return "MATCH"
        if in_metadata and pension_context:
            return "PARTIAL_MATCH"
        return "UNKNOWN"

    if in_core:
        return "MATCH"
    if in_metadata:
        return "PARTIAL_MATCH"
    # Explicitly different beneficiary groups are a mismatch; absent data is unknown.
    known_other_groups = [value for key, value in patterns.items() if key != target_group]
    if any(re.search(value, blob) for value in known_other_groups):
        return "NO_MATCH"
    return "UNKNOWN"


_CATEGORY_SCORE = {"MATCH": 1.0, "PARTIAL_MATCH": 0.65, "UNKNOWN": 0.25, "NO_MATCH": 0.0}
_CATEGORY_ORDER = {"MATCH": 0, "PARTIAL_MATCH": 1, "UNKNOWN": 2, "NO_MATCH": 3}


def rank_candidates(
    candidates: Sequence[tuple[Any, float]],
    profile: Optional[Mapping[str, Any]] = None,
    query: str = "",
    scheme_names: Optional[Sequence[str]] = None,
    intent: Optional[str] = None,
    target_group: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[RankedScheme]:
    """Rank ``(dataframe row, raw L2 distance)`` pairs conservatively.

    The eligibility checker is the sole eligibility engine. Its boolean result is
    never interpreted as definite eligibility when source criteria are incomplete.
    """
    w_semantic = RANK_WEIGHT_SEMANTIC if RERANKER_ENABLED else 1.0
    w_eligibility = RANK_WEIGHT_ELIGIBILITY if RERANKER_ENABLED else 0.0
    w_intent = RANK_WEIGHT_INTENT if RERANKER_ENABLED else 0.0
    known_names = [str(value) for value in (scheme_names or []) if value]
    query_lower = (query or "").lower()
    if target_group is None:
        try:
            from ..chat.intent import detect_target_group
        except ImportError:
            from chat.intent import detect_target_group
        target_group = detect_target_group(query)
    explicit_name = next((name for name in sorted(known_names, key=len, reverse=True) if name.lower() in query_lower), None)
    profile_values = {key: value for key, value in dict(profile or {}).items() if not key.startswith("_") and value is not None}
    request = _as_eligibility_request(profile_values)

    ranked: list[RankedScheme] = []
    for row, distance in candidates:
        name = str(row.get("scheme_name", ""))

        rejected = not is_eligible(request, row)
        if request.state and not is_state_compatible_before_scoring(request.state, row):
            rejected = True
        is_explicit_target = bool(explicit_name and name.casefold() == explicit_name.casefold())
        if rejected and not is_explicit_target:
            continue
        raw_match, reasons = calculate_match_score(request, row)
        missing = _missing_profile_fields(row, profile_values)
        has_criteria = bool(str(row.get("eligibility", "")).strip())
        if rejected:
            status, eligibility_score = "NOT_ELIGIBLE", 0.0
        elif not has_criteria or not profile_values:
            status, eligibility_score = "INSUFFICIENT_INFORMATION", 0.0
        else:
            status, eligibility_score = "POSSIBLY_ELIGIBLE", raw_match / 100.0

        distance = max(0.0, float(distance))
        semantic_similarity = 1.0 / (1.0 + distance)
        section_field = {
            "benefits": "benefits", "documents": "documents",
            "how_to_apply": "application", "check_eligibility": "eligibility",
            "scheme_details": "details",
        }.get(intent or "")
        intent_score = 1.0 if section_field and str(row.get(section_field, "")).strip() else 0.0
        exact_score = 1.0 if explicit_name and name.casefold() == explicit_name.casefold() else 0.0
        category_status = category_relevance(row, target_group)
        category_score = _CATEGORY_SCORE[category_status]
        final_score = (w_semantic * semantic_similarity + w_eligibility * eligibility_score
                       + w_intent * max(intent_score, exact_score)
                       + RANK_WEIGHT_CATEGORY * category_score)
        ranked.append(RankedScheme(
            row, float(distance), eligibility_score, final_score, status, reasons,
            missing, category_status, geographic_classification(row),
        ))

    ranked.sort(key=lambda item: (
        0 if explicit_name and str(item.scheme.get("scheme_name", "")).casefold() == explicit_name.casefold() else 1,
        _CATEGORY_ORDER[item.category_relevance] if target_group else 0,
        -item.final_score,
    ))
    if limit is None:
        limit = 1 if explicit_name else 3
    return ranked[:max(0, limit)]
