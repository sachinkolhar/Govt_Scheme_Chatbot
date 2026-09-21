"""Chat request processing."""
import json
import re
import sys
from typing import Generator, Optional

import pandas as pd

try:
    from ..config.settings import FAISS_MIN_SCORE, GROQ_API_KEY, NO_DATA_PROMPT
    from ..models.schemas import ChatRequest, ChatResponse, SchemeResult
    from ..search.semantic import get_dataframe
    from .groq_client import generate_answer_with_groq, stream_answer_with_groq
    from .state import conversation_key, get_chat_state, save_chat_state
except ImportError:
    from config.settings import FAISS_MIN_SCORE, GROQ_API_KEY, NO_DATA_PROMPT
    from models.schemas import ChatRequest, ChatResponse, SchemeResult
    from search.semantic import get_dataframe
    from chat.groq_client import generate_answer_with_groq, stream_answer_with_groq
    from chat.state import conversation_key, get_chat_state, save_chat_state


def _runtime_attr(name: str, default):
    """Allow legacy tests that monkeypatch backend.main helpers to keep working."""
    main_module = sys.modules.get("backend.main") or sys.modules.get("main")
    if main_module is not None and hasattr(main_module, name):
        return getattr(main_module, name)
    return default


def _semantic_candidates(query: str, top_k: int) -> list[tuple[int, float]]:
    try:
        from ..search.semantic import semantic_candidates
    except ImportError:
        from search.semantic import semantic_candidates

    return _runtime_attr("semantic_candidates", semantic_candidates)(query, top_k)


def _row_to_result(row: pd.Series, score: float = 0.0) -> SchemeResult:
    try:
        from ..search.semantic import row_to_result
    except ImportError:
        from search.semantic import row_to_result

    return _runtime_attr("row_to_result", row_to_result)(row, score)


def _get_db_relevant_schemes(query: str, limit: int = 5) -> list[SchemeResult]:
    try:
        from ..search.semantic import get_db_relevant_schemes
    except ImportError:
        from search.semantic import get_db_relevant_schemes

    return _runtime_attr("get_db_relevant_schemes", get_db_relevant_schemes)(query, limit=limit)


def _web_search_relevant_schemes(query: str, limit: int = 5) -> list[SchemeResult]:
    try:
        from ..search.web import web_search_relevant_schemes
    except ImportError:
        from search.web import web_search_relevant_schemes

    return _runtime_attr("web_search_relevant_schemes", web_search_relevant_schemes)(
        query, limit=limit
    )


def _summarize_web_schemes_with_groq(query: str, schemes: list[SchemeResult]) -> str:
    try:
        from ..search.web import summarize_web_schemes_with_groq
    except ImportError:
        from search.web import summarize_web_schemes_with_groq

    return _runtime_attr("summarize_web_schemes_with_groq", summarize_web_schemes_with_groq)(
        query, schemes
    )


def _generate_answer_with_groq(query: str, scheme: pd.Series, history=None) -> str:
    return _runtime_attr("generate_answer_with_groq", generate_answer_with_groq)(
        query, scheme, history
    )


def detect_requested_section(query: str) -> Optional[str]:
    lowered = query.lower()
    section_patterns = {
        "eligibility": ["eligibility", "eligible", "who can apply", "am i eligible"],
        "application": ["how to apply", "apply", "application process", "steps to apply"],
        "benefits": ["benefits", "advantage", "what do i get"],
        "documents": ["documents", "document required", "papers required"],
        "details": ["details", "about this scheme", "overview", "what is this"],
    }
    for section, patterns in section_patterns.items():
        if any(pattern in lowered for pattern in patterns):
            return section
    return None


def is_yes_reply(query: str) -> bool:
    cleaned = re.sub(r"^[\s.!?\u0964]+|[\s.!?\u0964]+$", "", query.lower())
    cleaned = re.sub(r"\s+", " ", cleaned)
    yes_replies = {
        "yes",
        "y",
        "yeah",
        "yep",
        "sure",
        "ok",
        "okay",
        "haan",
        "han",
        "ji",
        "\u0939\u093e\u0901",
        "\u0939\u093e\u0902",
        "\u0939\u093e",
        "\u091c\u0940",
    }
    return cleaned in yes_replies


def is_no_reply(query: str) -> bool:
    cleaned = re.sub(r"^[\s.!?\u0964]+|[\s.!?\u0964]+$", "", query.lower())
    cleaned = re.sub(r"\s+", " ", cleaned)
    no_replies = {
        "no",
        "n",
        "nope",
        "nah",
        "nahi",
        "na",
        "\u0928\u0939\u0940\u0902",
        "\u0928\u0939\u0940",
        "\u0928\u093e",
    }
    return cleaned in no_replies


def section_value(scheme: pd.Series, section: str) -> str:
    section_map = {
        "eligibility": str(scheme.get("eligibility", "Not specified")),
        "application": str(scheme.get("application", "Not specified")),
        "benefits": str(scheme.get("benefits", "Not specified")),
        "documents": str(scheme.get("documents", "Not specified")),
        "details": str(scheme.get("details", "Not specified")),
    }
    return section_map.get(section, str(scheme.get("details", "Not specified")))


def build_section_only_answer(scheme: pd.Series, section: str) -> str:
    label_map = {
        "eligibility": "Eligibility",
        "application": "How to Apply",
        "benefits": "Benefits",
        "documents": "Documents Required",
        "details": "Details",
    }
    label = label_map.get(section, "Details")
    return (
        f"**Scheme:** {str(scheme.get('scheme_name', 'N/A'))}\n\n"
        f"**{label}**\n{section_value(scheme, section)}"
    )


def process_chat(payload: ChatRequest) -> ChatResponse:
    key = conversation_key(payload)
    state = get_chat_state(key)
    query = payload.query.strip()

    if state.pending_relevant_suggestions and is_no_reply(query):
        state.pending_relevant_suggestions = False
        save_chat_state(key, state)
        return ChatResponse(
            query=payload.query,
            answer="No problem. Ask me about any other scheme whenever you want.",
            response_type="direct_answer",
            source_scheme=None,
        )

    if state.pending_relevant_suggestions and is_yes_reply(query):
        db_results = _get_db_relevant_schemes(state.last_query or payload.query, limit=5)
        used_web = False
        relevant = db_results
        if not relevant:
            relevant = _web_search_relevant_schemes(state.last_query or payload.query, limit=5)
            used_web = True
        state.pending_relevant_suggestions = False
        save_chat_state(key, state)
        if relevant:
            answer = (
                _summarize_web_schemes_with_groq(state.last_query or payload.query, relevant)
                if used_web
                else f"Here are {len(relevant)} relevant schemes for you."
            )
            return ChatResponse(
                query=payload.query,
                answer=answer,
                response_type="relevant_schemes",
                source_scheme=None,
                relevant_schemes=relevant,
            )
        return ChatResponse(
            query=payload.query,
            answer="Sorry, I could not find relevant schemes right now.",
            response_type="direct_answer",
            source_scheme=None,
        )

    candidates = _semantic_candidates(query, max(payload.top_k, 5))
    has_confident_match = bool(candidates) and candidates[0][1] >= FAISS_MIN_SCORE
    if not has_confident_match:
        state.pending_relevant_suggestions = True
        state.last_query = query
        save_chat_state(key, state)
        return ChatResponse(
            query=payload.query,
            answer=NO_DATA_PROMPT,
            response_type="no_data_prompt",
            source_scheme=None,
        )

    idx, score = candidates[0]
    scheme = get_dataframe().iloc[idx]
    requested_section = detect_requested_section(query)
    if requested_section:
        answer = build_section_only_answer(scheme, requested_section)
    else:
        answer = _generate_answer_with_groq(payload.query, scheme, payload.history)

    state.pending_relevant_suggestions = False
    save_chat_state(key, state)
    return ChatResponse(
        query=payload.query,
        answer=answer,
        response_type="direct_answer",
        source_scheme=_row_to_result(scheme, score),
    )


def stream_chat_events(payload: ChatRequest) -> Generator[str, None, None]:
    key = conversation_key(payload)
    state = get_chat_state(key)
    query = payload.query.strip()

    if state.pending_relevant_suggestions and is_no_reply(query):
        state.pending_relevant_suggestions = False
        save_chat_state(key, state)
        yield f"data: {json.dumps({'type': 'response_type', 'value': 'direct_answer'})}\n\n"
        yield f"data: {json.dumps({'type': 'token', 'text': 'No problem. Ask me about any other scheme whenever you want.'})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return

    if state.pending_relevant_suggestions and is_yes_reply(query):
        db_results = _get_db_relevant_schemes(state.last_query or payload.query, limit=5)
        used_web = False
        relevant = db_results
        if not relevant:
            relevant = _web_search_relevant_schemes(state.last_query or payload.query, limit=5)
            used_web = True
        state.pending_relevant_suggestions = False
        save_chat_state(key, state)
        if relevant:
            lead_text = (
                _summarize_web_schemes_with_groq(state.last_query or payload.query, relevant)
                if used_web
                else f"Here are {len(relevant)} relevant schemes for you."
            )
            yield f"data: {json.dumps({'type': 'response_type', 'value': 'relevant_schemes'})}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'text': lead_text})}\n\n"
            yield f"data: {json.dumps({'type': 'relevant_schemes', 'data': [item.model_dump() for item in relevant]})}\n\n"
        else:
            yield f"data: {json.dumps({'type': 'response_type', 'value': 'direct_answer'})}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'text': 'Sorry, I could not find relevant schemes right now.'})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return

    candidates = _semantic_candidates(query, max(payload.top_k, 5))
    has_confident_match = bool(candidates) and candidates[0][1] >= FAISS_MIN_SCORE

    if not has_confident_match:
        state.pending_relevant_suggestions = True
        state.last_query = query
        save_chat_state(key, state)
        yield f"data: {json.dumps({'type': 'response_type', 'value': 'no_data_prompt'})}\n\n"
        yield f"data: {json.dumps({'type': 'token', 'text': NO_DATA_PROMPT})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return

    idx, score = candidates[0]
    scheme = get_dataframe().iloc[idx]
    source_scheme = _row_to_result(scheme, score)
    scheme_event = f"data: {json.dumps({'type': 'scheme', 'data': source_scheme.model_dump()})}\n\n"
    requested_section = detect_requested_section(query)

    yield f"data: {json.dumps({'type': 'response_type', 'value': 'direct_answer'})}\n\n"
    if requested_section:
        section_answer = build_section_only_answer(scheme, requested_section)
        yield f"data: {json.dumps({'type': 'token', 'text': section_answer})}\n\n"
        yield scheme_event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        state.pending_relevant_suggestions = False
        save_chat_state(key, state)
        return

    if not GROQ_API_KEY:
        fallback = (
            f"**Scheme:** {str(scheme.get('scheme_name', 'N/A'))}\n\n"
            f"**Eligibility**\n{str(scheme.get('eligibility', 'Not specified'))}\n\n"
            f"**Benefits**\n{str(scheme.get('benefits', 'Not specified'))}\n\n"
            f"**How to Apply**\n{str(scheme.get('application', 'Not specified'))}"
        )
        yield f"data: {json.dumps({'type': 'token', 'text': fallback})}\n\n"
        yield scheme_event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        state.pending_relevant_suggestions = False
        save_chat_state(key, state)
        return

    try:
        groq_stream = stream_answer_with_groq(payload.query, payload.history, scheme)
        for chunk in groq_stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield f"data: {json.dumps({'type': 'token', 'text': delta})}\n\n"
        yield scheme_event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    except Exception as exc:
        yield f"data: {json.dumps({'type': 'error', 'text': str(exc)})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    state.pending_relevant_suggestions = False
    save_chat_state(key, state)
