"""Confidence bands and one-question-at-a-time clarification helpers."""
try:
    from ..config.settings import CONFIDENCE_HIGH_THRESHOLD, CONFIDENCE_MEDIUM_THRESHOLD
except ImportError:
    from config.settings import CONFIDENCE_HIGH_THRESHOLD, CONFIDENCE_MEDIUM_THRESHOLD


_QUESTIONS = {
    "age": "How old are you?",
    "state": "Which state do you live in?",
    "income": "What is your annual family income?",
    "occupation": "What is your occupation?",
    "category": "What is your category, if relevant?",
}


def confidence_band(score: float) -> str:
    if score >= CONFIDENCE_HIGH_THRESHOLD:
        return "HIGH_CONFIDENCE"
    if score >= CONFIDENCE_MEDIUM_THRESHOLD:
        return "MEDIUM_CONFIDENCE"
    return "LOW_CONFIDENCE"


def begin_clarification(state, original_query: str, required_fields: list[str], candidates: list[dict] | None = None) -> str:
    field = next((item for item in ("state", "age", "income", "occupation", "category") if item in required_fields), None)
    if field is None:
        state.pending_question = None
        state.required_field = None
        return ""
    state.pending_question = _QUESTIONS[field]
    state.required_field = field
    state.clarification_context = original_query
    state.last_query = original_query
    state.previous_candidates = candidates or []
    return state.pending_question


def accept_clarification_reply(state, reply: str) -> dict:
    """Extract the answer while preserving original query and candidate context."""
    try:
        from .facts import extract_user_facts
    except ImportError:
        from chat.facts import extract_user_facts
    result = extract_user_facts(reply)
    field = state.required_field
    if field == "age" and "age" not in result:
        import re
        age_reply = re.fullmatch(r"\s*(\d{1,3})\s*(?:years?(?: old)?)?\s*", reply, flags=re.IGNORECASE)
        if age_reply and 0 < int(age_reply.group(1)) < 125:
            result["age"] = int(age_reply.group(1))
    if field and field in result:
        state.collected_facts[field] = result[field]
        state.pending_question = None
        state.required_field = None
    return {
        "original_query": state.clarification_context or state.last_query,
        "facts": dict(state.collected_facts),
        "pending_question": state.pending_question,
        "required_field": state.required_field,
        "previous_candidates": list(state.previous_candidates),
    }
