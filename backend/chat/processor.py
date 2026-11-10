"""Chat request processing."""
import json
import logging
import re
import sys
import time
from typing import Generator, Optional

import pandas as pd

logger = logging.getLogger(__name__)

try:
    from ..config.settings import CHAT_TOP_N, GROQ_API_KEY, NO_DATA_PROMPT, RERANKER_ENABLED, SEMANTIC_RETRIEVAL_TOP_K, WEB_SEARCH_ENABLED
    from ..models.schemas import ChatRequest, ChatResponse, SchemeResult
    from ..search.semantic import get_dataframe
    from ..search.geography import geographic_applicability, geographic_classification, is_geographically_applicable
    from ..search.candidate_selection import deduplicate_schemes
    from ..search.ranking import category_relevance
    from .groq_client import generate_answer_with_groq, stream_answer_with_groq
    from .state import conversation_key, get_chat_state, save_chat_state
    from .facts import extract_user_facts
    from .intent import detect_intent, detect_target_group
    from .clarification import accept_clarification_reply, begin_clarification
    from .pipeline import CandidateResolution, resolve_scheme_candidates
    from .query_normalization import normalize_query_for_retrieval, query_for_answer_language
except ImportError:
    from config.settings import CHAT_TOP_N, GROQ_API_KEY, NO_DATA_PROMPT, RERANKER_ENABLED, SEMANTIC_RETRIEVAL_TOP_K, WEB_SEARCH_ENABLED
    from models.schemas import ChatRequest, ChatResponse, SchemeResult
    from search.semantic import get_dataframe
    from search.geography import geographic_applicability, geographic_classification, is_geographically_applicable
    from search.candidate_selection import deduplicate_schemes
    from search.ranking import category_relevance
    from chat.groq_client import generate_answer_with_groq, stream_answer_with_groq
    from chat.state import conversation_key, get_chat_state, save_chat_state
    from chat.facts import extract_user_facts
    from chat.intent import detect_intent, detect_target_group
    from chat.clarification import accept_clarification_reply, begin_clarification
    from chat.pipeline import CandidateResolution, resolve_scheme_candidates
    from chat.query_normalization import normalize_query_for_retrieval, query_for_answer_language


def _runtime_attr(name: str, default):
    """Allow legacy tests that monkeypatch backend.main helpers to keep working."""
    main_module = sys.modules.get("backend.main") or sys.modules.get("main")
    if main_module is not None and hasattr(main_module, name):
        return getattr(main_module, name)
    return default


def _semantic_candidates(query: str, top_k: int) -> list[tuple[int, float]]:
    try:
        from ..search.semantic import hybrid_candidates, semantic_candidates
    except ImportError:
        from search.semantic import hybrid_candidates, semantic_candidates

    # Keep legacy monkeypatches/integrations working; normal traffic uses hybrid retrieval.
    configured = _runtime_attr("semantic_candidates", semantic_candidates)
    if configured is not semantic_candidates:
        return configured(query, top_k)
    return hybrid_candidates(query, top_k)


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


def _web_query_for_state(state, fallback: str) -> str:
    original = state.pending_original_query or state.last_query or fallback
    user_state = state.collected_facts.get("state")
    suffix = "official government"
    if user_state:
        suffix += f" {user_state} site:gov.in OR site:nic.in OR site:india.gov.in OR site:myscheme.gov.in"
    return f"{original} {suffix}"


def _filter_web_schemes(schemes: list[SchemeResult], query: str, state) -> list[SchemeResult]:
    """Apply the same location and beneficiary constraints to official results."""
    user_state = state.collected_facts.get("state")
    target_group = state.target_group_context or detect_target_group(query)
    accepted = []
    for scheme in schemes:
        row = scheme.model_dump() if hasattr(scheme, "model_dump") else dict(scheme)
        if user_state and geographic_applicability(row, str(user_state)) != "applicable":
            continue
        if target_group and category_relevance(row, target_group) not in {"MATCH", "PARTIAL_MATCH"}:
            continue
        query_terms = set(re.findall(r"[a-z0-9]+", query.casefold()))
        query_terms.difference_update({
            "the", "for", "a", "an", "and", "or", "in", "of", "to", "scheme", "schemes",
            "government", "official", "search", "india", "state", "central",
            re.sub(r"[^a-z0-9]+", " ", str(user_state or "").casefold()).strip(),
        })
        evidence = " ".join(str(row.get(field, "") or "") for field in (
            "scheme_name", "details", "benefits", "eligibility", "schemeCategory", "tags",
        )).casefold()
        # A lone residual term is often a paraphrase or an underspecified query
        # (and web search has already ranked the result). Only apply this lexical
        # guard when the user supplied multiple meaningful concepts.
        if len(query_terms) >= 2 and not (query_terms & set(re.findall(r"[a-z0-9]+", evidence))):
            continue
        accepted.append(scheme)
    return deduplicate_schemes(accepted)


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


def _grounding_row(candidate, user_state: Optional[str] = None) -> pd.Series:
    row = candidate.scheme.copy()
    row["eligibility_result"] = candidate.eligibility_status
    row["missing_information"] = ", ".join(candidate.missing_information) or "None identified"
    row["geographic_classification"] = candidate.geography or geographic_classification(row)
    row["user_state_context"] = user_state or ""
    row["target_group_relevance"] = candidate.category_relevance
    return row


def _prepare_resolution(query: str, payload: ChatRequest, state) -> tuple[Optional[CandidateResolution], str, bool]:
    """Resolve one turn through the shared retrieval and ranking pipeline.

    Returns (resolution, clarification_text, is_clarification_pending).
    """
    is_reply = bool(state.pending_question)
    current_facts = extract_user_facts(query)
    if is_reply:
        accepted = accept_clarification_reply(state, query)
        if accepted["required_field"]:
            return None, accepted["pending_question"], True
        query_for_pipeline = accepted["original_query"]
        profile = dict(state.collected_facts)
    else:
        query_for_pipeline = normalize_query_for_retrieval(query)
        profile = dict(state.collected_facts)
        profile.update({key: value for key, value in current_facts.items() if not key.startswith("_")})
        state.collected_facts = profile

    dataframe = get_dataframe()
    names = [str(name) for name in dataframe.get("scheme_name", pd.Series(dtype=str)).tolist()]
    current_intent = detect_intent(query_for_pipeline, names)
    resolved_name = None
    if current_intent.intent == "follow_up" and not state.last_query and not is_reply:
        candidate_indices = []
    else:
        candidate_indices = None
    if not is_reply and state.last_query and not current_intent.scheme_name and (
        current_intent.requested_section or current_intent.intent == "follow_up"
    ):
        candidates = [item.get("scheme_name", "") for item in state.previous_candidates if isinstance(item, dict)]
        ordinal = re.search(r"\b(second|2nd|third|3rd|first|1st)\b", query.lower())
        if ordinal and len(candidates) > 1:
            position = {"first": 0, "1st": 0, "second": 1, "2nd": 1, "third": 2, "3rd": 2}[ordinal.group(1)]
            if position < len(candidates):
                selected_name = candidates[position]
                resolved_name = selected_name
                query_for_pipeline = f"{selected_name} {query}"
                current_intent = detect_intent(query_for_pipeline, names)
        ambiguous_reference = any(phrase in query.lower() for phrase in ("this one", "that one")) and len(candidates) > 1
        if ambiguous_reference:
            options = " or ".join(candidates[:3])
            return None, f"Which scheme do you mean — {options}?", True
        prior_name = resolved_name or next((name for name in candidates if name), state.active_scheme_name or "")
        query_for_pipeline = f"{prior_name or ''} {query_for_pipeline}".strip()
        contextual_intent = detect_intent(query_for_pipeline, names)
        current_intent = type(current_intent)(
            current_intent.intent,
            current_intent.confidence,
            contextual_intent.scheme_name,
            current_intent.requested_section,
            current_intent.target_group or contextual_intent.target_group,
        )

    if not current_intent.target_group and state.target_group_context and (
        current_intent.requested_section or current_intent.intent == "follow_up"
    ):
        current_intent = type(current_intent)(
            current_intent.intent, current_intent.confidence, current_intent.scheme_name,
            current_intent.requested_section, state.target_group_context,
        )
        group_query = {
            "senior_citizen": "senior citizen old age",
            "construction_worker": "construction worker",
            "farmer": "farmer",
            "student": "student",
            "women": "women",
            "disability": "disability",
            "worker": "worker",
        }.get(state.target_group_context, "")
        query_for_pipeline = f"{query_for_pipeline} {group_query}".strip()

    top_k = max(payload.top_k, CHAT_TOP_N, SEMANTIC_RETRIEVAL_TOP_K)
    if profile.get("state"):
        query_for_pipeline = f"{query_for_pipeline} {profile['state']}".strip()
    if candidate_indices is None:
        candidate_indices = _semantic_candidates(query_for_pipeline, top_k)
    if profile.get("state"):
        candidate_indices = [
            candidate for candidate in candidate_indices
            if 0 <= int(candidate[0]) < len(dataframe)
            and is_geographically_applicable(dataframe.iloc[int(candidate[0])], str(profile["state"]))
        ]
    if current_intent.scheme_name and not resolved_name:
        named_scheme = current_intent.scheme_name.casefold()
        candidate_indices = [
            candidate for candidate in candidate_indices
            if 0 <= int(candidate[0]) < len(dataframe)
            and str(dataframe.iloc[int(candidate[0])].get("scheme_name", "")).casefold() == named_scheme
        ]
    if resolved_name:
        candidate_indices = [
            candidate for candidate in candidate_indices
            if 0 <= int(candidate[0]) < len(dataframe)
            and str(dataframe.iloc[int(candidate[0])].get("scheme_name", "")).casefold() == resolved_name.casefold()
        ]
    resolution = resolve_scheme_candidates(
        query_for_pipeline,
        profile=profile,
        intent=current_intent if not is_reply else detect_intent(query_for_pipeline, names),
        scheme_names=names,
        top_k=top_k,
        candidate_indices=candidate_indices,
        dataframe=dataframe,
    )
    if resolution.intent.target_group:
        state.target_group_context = resolution.intent.target_group

    missing = list(resolution.missing_information)
    if resolution.intent.intent == "find_scheme" and not profile.get("state"):
        missing.insert(0, "state")
    personal_eligibility = resolution.intent.intent == "check_eligibility" and any(
        phrase in query_for_pipeline.lower()
        for phrase in ("can i get", "am i eligible", "do i qualify")
    )
    clarification_fields = missing if personal_eligibility else (["state"] if resolution.intent.intent == "find_scheme" and not profile.get("state") else [])
    if resolution.candidates and resolution.confidence != "LOW_CONFIDENCE" and clarification_fields:
        question = begin_clarification(
            state,
            query_for_pipeline,
            clarification_fields,
            [{"scheme_name": str(item.scheme.get("scheme_name", ""))} for item in resolution.candidates],
        )
        if question:
            return resolution, question, True
    if is_reply:
        state.pending_question = None
        state.required_field = None
        state.clarification_context = ""
    return resolution, "", False


def _resolve_yes_fallback(payload: ChatRequest, state) -> tuple[list[SchemeResult], bool, str]:
    """Use the shared local resolution before web fallback on explicit consent."""
    original_query = state.pending_original_query or state.last_query or payload.query
    # Preserve the legacy generic suggestion path only when the conversation has
    # no geographic or target-group constraint to bypass. Constrained requests
    # always go through the shared candidate resolver below.
    if (
        not state.collected_facts.get("state")
        and not (state.target_group_context or detect_target_group(original_query))
        and state.pending_action != "official_web_search"
    ):
        generic = deduplicate_schemes(_get_db_relevant_schemes(original_query, limit=5))
        if generic:
            return generic, False, original_query
        if WEB_SEARCH_ENABLED:
            web_query = _web_query_for_state(state, original_query)
            results = _web_search_relevant_schemes(web_query, limit=5)
            return _filter_web_schemes(results, original_query, state), True, web_query
        return [], False, original_query
    contextual_payload = payload.model_copy(update={"query": original_query})
    resolution, _, _ = _prepare_resolution(original_query, contextual_payload, state)
    if resolution:
        state.last_query = resolution.query
        if resolution.intent.target_group:
            state.target_group_context = resolution.intent.target_group
    if resolution and resolution.candidates and resolution.confidence != "LOW_CONFIDENCE":
        return [
            _row_to_result(item.scheme, item.semantic_score)
            for item in resolution.candidates
        ], False, original_query
    if WEB_SEARCH_ENABLED:
        web_query = _web_query_for_state(state, original_query)
        results = _web_search_relevant_schemes(web_query, limit=5)
        return _filter_web_schemes(results, original_query, state), True, web_query
    return [], False, original_query


def process_chat(payload: ChatRequest) -> ChatResponse:
    started_at = time.perf_counter()
    key = conversation_key(payload)
    state = get_chat_state(key)
    state.conversation_id = key
    state.language = payload.language or "en"
    query = payload.query.strip()

    if state.pending_relevant_suggestions and is_no_reply(query):
        state.pending_relevant_suggestions = False
        state.pending_action = None
        state.pending_original_query = None
        save_chat_state(key, state)
        return ChatResponse(
            query=payload.query,
            answer="No problem. Ask me about any other scheme whenever you want.",
            response_type="direct_answer",
            source_scheme=None,
        )

    if state.pending_relevant_suggestions and is_yes_reply(query):
        relevant, used_web, fallback_query = _resolve_yes_fallback(payload, state)
        state.pending_relevant_suggestions = False
        state.pending_action = None
        state.pending_original_query = None
        save_chat_state(key, state)
        if relevant:
            answer = (
                _summarize_web_schemes_with_groq(
                    query_for_answer_language(fallback_query, payload.language), relevant
                )
                if used_web
                else f"Here are {len(relevant)} relevant schemes for you."
            )
            return ChatResponse(
                query=payload.query,
                answer=answer,
                response_type="relevant_schemes",
                source_scheme=None,
                relevant_schemes=relevant,
                sources=[
                    {"title": item.source_title or item.scheme_name, "url": item.source_url,
                     "source_type": item.source_type or "official", "retrieved_at": item.retrieved_at}
                    for item in relevant if item.source_url
                ],
            )
        return ChatResponse(
            query=payload.query,
            answer="Sorry, I could not find relevant schemes right now.",
            response_type="direct_answer",
            source_scheme=None,
        )

    resolution, clarification, needs_clarification = _prepare_resolution(query, payload, state)
    state.last_user_query = query
    logger.info(
        "chat retrieval completed",
        extra={
            "conversation_id": key,
            "intent": resolution.intent.intent if resolution else "clarification",
            "retrieval_method": "hybrid_faiss_bm25",
            "candidate_count": len(resolution.candidates) if resolution else 0,
            "selected_scheme_names": [str(item.scheme.get("scheme_name", "")) for item in resolution.candidates] if resolution else [],
            "reranker_enabled": RERANKER_ENABLED,
            "model": "groq" if GROQ_API_KEY else "structured_fallback",
            "fallback_reason": "clarification" if needs_clarification else ("low_confidence" if not resolution or resolution.confidence == "LOW_CONFIDENCE" else None),
            "latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
        },
    )
    if needs_clarification:
        save_chat_state(key, state)
        return ChatResponse(
            query=payload.query,
            answer=clarification,
            response_type="clarification",
            source_scheme=None,
        )
    if not resolution or not resolution.candidates or resolution.confidence == "LOW_CONFIDENCE":
        state.pending_relevant_suggestions = True
        state.last_query = resolution.query if resolution else (state.clarification_context or query)
        state.pending_action = "official_web_search"
        state.pending_original_query = state.last_query
        save_chat_state(key, state)
        return ChatResponse(
            query=payload.query,
            answer=NO_DATA_PROMPT,
            response_type="no_data_prompt",
            source_scheme=None,
        )

    ranked = resolution.candidates
    selected = ranked[0]
    scheme = selected.scheme
    score = selected.semantic_score
    requested_section = resolution.intent.requested_section or detect_requested_section(query)
    if requested_section:
        answer = build_section_only_answer(scheme, requested_section)
    else:
        answer_query = query_for_answer_language(query, payload.language)
        answer = _generate_answer_with_groq(
            answer_query,
            _grounding_row(selected, resolution.facts.get("state")),
            payload.history,
        )

    state.pending_relevant_suggestions = False
    state.last_query = resolution.query
    state.previous_candidates = [{"scheme_name": str(item.scheme.get("scheme_name", ""))} for item in ranked]
    state.last_intent = resolution.intent.intent
    state.rewritten_query = resolution.query
    state.active_scheme_name = str(scheme.get("scheme_name", ""))
    state.active_scheme_id = None
    state.recent_retrieved_scheme_ids = []
    save_chat_state(key, state)
    return ChatResponse(
        query=payload.query,
        answer=answer,
        response_type="direct_answer",
        source_scheme=_row_to_result(scheme, score),
        relevant_schemes=[_row_to_result(item.scheme, item.semantic_score) for item in ranked],
    )


def stream_chat_events(payload: ChatRequest) -> Generator[str, None, None]:
    key = conversation_key(payload)
    state = get_chat_state(key)
    state.conversation_id = key
    state.language = payload.language or "en"
    query = payload.query.strip()

    if state.pending_relevant_suggestions and is_no_reply(query):
        state.pending_relevant_suggestions = False
        state.pending_action = None
        state.pending_original_query = None
        save_chat_state(key, state)
        yield f"data: {json.dumps({'type': 'response_type', 'value': 'direct_answer'})}\n\n"
        yield f"data: {json.dumps({'type': 'token', 'text': 'No problem. Ask me about any other scheme whenever you want.'})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return

    if state.pending_relevant_suggestions and is_yes_reply(query):
        relevant, used_web, fallback_query = _resolve_yes_fallback(payload, state)
        state.pending_relevant_suggestions = False
        state.pending_action = None
        state.pending_original_query = None
        save_chat_state(key, state)
        if relevant:
            lead_text = (
                _summarize_web_schemes_with_groq(
                    query_for_answer_language(fallback_query, payload.language), relevant
                )
                if used_web
                else f"Here are {len(relevant)} relevant schemes for you."
            )
            yield f"data: {json.dumps({'type': 'response_type', 'value': 'relevant_schemes'})}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'text': lead_text})}\n\n"
            yield f"data: {json.dumps({'type': 'relevant_schemes', 'data': [item.model_dump() for item in relevant]})}\n\n"
            source_rows = [
                {"title": item.source_title or item.scheme_name, "url": item.source_url,
                 "source_type": item.source_type or "official", "retrieved_at": item.retrieved_at}
                for item in relevant if item.source_url
            ]
            if source_rows:
                yield f"data: {json.dumps({'type': 'sources', 'data': source_rows})}\n\n"
        else:
            yield f"data: {json.dumps({'type': 'response_type', 'value': 'direct_answer'})}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'text': 'Sorry, I could not find relevant schemes right now.'})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return

    resolution, clarification, needs_clarification = _prepare_resolution(query, payload, state)
    state.last_user_query = query
    if needs_clarification:
        save_chat_state(key, state)
        yield f"data: {json.dumps({'type': 'response_type', 'value': 'clarification'})}\n\n"
        yield f"data: {json.dumps({'type': 'token', 'text': clarification})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return

    if not resolution or not resolution.candidates or resolution.confidence == "LOW_CONFIDENCE":
        state.pending_relevant_suggestions = True
        state.last_query = resolution.query if resolution else (state.clarification_context or query)
        state.pending_action = "official_web_search"
        state.pending_original_query = state.last_query
        save_chat_state(key, state)
        yield f"data: {json.dumps({'type': 'response_type', 'value': 'no_data_prompt'})}\n\n"
        yield f"data: {json.dumps({'type': 'token', 'text': NO_DATA_PROMPT})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return

    ranked = resolution.candidates
    selected = ranked[0]
    scheme = selected.scheme
    score = selected.semantic_score
    source_scheme = _row_to_result(scheme, score)
    scheme_event = f"data: {json.dumps({'type': 'scheme', 'data': source_scheme.model_dump()})}\n\n"
    ranked_event = f"data: {json.dumps({'type': 'relevant_schemes', 'data': [_row_to_result(item.scheme, item.semantic_score).model_dump() for item in ranked]})}\n\n"
    requested_section = resolution.intent.requested_section or detect_requested_section(query)

    yield f"data: {json.dumps({'type': 'response_type', 'value': 'direct_answer'})}\n\n"
    if requested_section:
        section_answer = build_section_only_answer(scheme, requested_section)
        yield f"data: {json.dumps({'type': 'token', 'text': section_answer})}\n\n"
        yield scheme_event
        yield ranked_event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        state.pending_relevant_suggestions = False
        state.last_query = resolution.query
        state.previous_candidates = [{"scheme_name": str(item.scheme.get("scheme_name", ""))} for item in ranked]
        state.last_intent = resolution.intent.intent
        state.rewritten_query = resolution.query
        state.active_scheme_name = str(scheme.get("scheme_name", ""))
        save_chat_state(key, state)
        return

    if not GROQ_API_KEY:
        fallback = (
            f"**Scheme:** {str(scheme.get('scheme_name', 'N/A'))}\n\n"
            f"**Details**\n{str(scheme.get('details', 'Information unavailable in retrieved records.'))}"
        )
        yield f"data: {json.dumps({'type': 'token', 'text': fallback})}\n\n"
        yield scheme_event
        yield ranked_event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        state.pending_relevant_suggestions = False
        state.last_query = resolution.query
        state.previous_candidates = [{"scheme_name": str(item.scheme.get("scheme_name", ""))} for item in ranked]
        state.last_intent = resolution.intent.intent
        state.rewritten_query = resolution.query
        state.active_scheme_name = str(scheme.get("scheme_name", ""))
        save_chat_state(key, state)
        return

    try:
        groq_stream = stream_answer_with_groq(
            query_for_answer_language(query, payload.language), payload.history,
            _grounding_row(selected, resolution.facts.get("state")),
        )
        for chunk in groq_stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield f"data: {json.dumps({'type': 'token', 'text': delta})}\n\n"
        yield scheme_event
        yield ranked_event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    except Exception:
        fallback = (
            f"**Scheme:** {str(scheme.get('scheme_name', 'N/A'))}\n\n"
            f"**Details**\n{str(scheme.get('details', 'Information unavailable in retrieved records.'))}"
        )
        yield f"data: {json.dumps({'type': 'token', 'text': fallback})}\n\n"
        yield scheme_event
        yield ranked_event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    state.pending_relevant_suggestions = False
    state.last_query = resolution.query
    state.previous_candidates = [{"scheme_name": str(item.scheme.get("scheme_name", ""))} for item in ranked]
    state.last_intent = resolution.intent.intent
    state.rewritten_query = resolution.query
    state.active_scheme_name = str(scheme.get("scheme_name", ""))
    save_chat_state(key, state)
