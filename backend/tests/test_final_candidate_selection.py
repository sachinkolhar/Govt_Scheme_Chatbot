import pandas as pd

import backend.main as main
import backend.search.semantic as semantic
from backend.chat.state import get_chat_state
from backend.search.candidate_selection import deduplicate_schemes, scheme_identity
from backend.search.geography import geographic_applicability, geographic_classification
from backend.search.ranking import category_relevance


def _actual_rows(*names):
    data = pd.read_csv("dataset/govt_schemes.csv")
    return [data.loc[data.scheme_name.eq(name)].iloc[0] for name in names]


def test_central_and_unknown_geography_are_distinct():
    central, unknown = _actual_rows(
        "NSAP - Indira Gandhi National Old Age Pension Scheme",
        "Incentive For The Intra Caste Marriage within Scheduled Tribe Community",
    )
    assert geographic_classification(central) == "CENTRAL"
    assert geographic_applicability(central, "Karnataka") == "applicable"
    unknown_row = {column: "" for column in unknown.index}
    unknown_row.update({"scheme_name": "Unscoped test record", "details": "A scheme with no stated geographic scope."})
    assert geographic_classification(unknown_row) == "UNKNOWN"
    assert geographic_applicability(unknown_row, "Karnataka") == "unknown"


def test_normalized_identity_dedupes_aliases_but_keeps_distinct_schemes():
    first = {"scheme_name": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)", "level": "Central"}
    duplicate = {"scheme_name": "  INDIRA-GANDHI National Old Age Pension Scheme  ", "level": "Central"}
    assert scheme_identity(first) == scheme_identity(duplicate)
    assert len(deduplicate_schemes([first, duplicate])) == 1

    worker_pension, worker_continuation = _actual_rows(
        "Pension Scheme (K.B.O.C.W.W.B)",
        "Continuation of Pension (K.B.O.C.W.W.B)",
    )
    assert scheme_identity(worker_pension) != scheme_identity(worker_continuation)


def test_only_final_category_matches_reach_response_and_llm(monkeypatch):
    central, worker, continuation, law_graduate = _actual_rows(
        "NSAP - Indira Gandhi National Old Age Pension Scheme",
        "Pension Scheme (K.B.O.C.W.W.B)",
        "Continuation of Pension (K.B.O.C.W.W.B)",
        "Stipend To Law Graduates",
    )
    duplicate_central = central.copy()
    duplicate_central["scheme_name"] = "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)"
    frame = pd.DataFrame([worker, law_graduate, continuation, central, duplicate_central])
    monkeypatch.setattr(semantic, "df", frame)
    monkeypatch.setattr(main, "semantic_candidates", lambda _query, _k: [(0, 0.01), (1, 0.02), (2, 0.03), (3, 0.2), (4, 0.25)])

    grounded = {}

    def answer(query, scheme, _history=None):
        grounded["query"] = query
        grounded["scheme"] = scheme.copy()
        return "Central scheme summary."

    monkeypatch.setattr(main, "generate_answer_with_groq", answer)
    main.chat_state_store.clear()
    first = main.chat(main.ChatRequest(query="senior citizen pension scheme", conversation_id="final-candidate-set"))
    assert first.response_type == "clarification"
    response = main.chat(main.ChatRequest(query="Karnataka", conversation_id="final-candidate-set"))

    assert response.response_type == "direct_answer"
    assert response.source_scheme.scheme_name == central.scheme_name
    assert [item.scheme_name for item in response.relevant_schemes] == [central.scheme_name]
    assert category_relevance(worker, "senior_citizen") == "NO_MATCH"
    assert category_relevance(continuation, "senior_citizen") == "NO_MATCH"
    assert category_relevance(law_graduate, "senior_citizen") == "NO_MATCH"
    assert grounded["scheme"].scheme_name == central.scheme_name
    assert grounded["scheme"]["geographic_classification"] == "CENTRAL"
    assert grounded["scheme"]["user_state_context"] == "Karnataka"
    assert "Karnataka" in grounded["query"]
    assert get_chat_state("final-candidate-set").collected_facts["state"] == "Karnataka"


def test_duplicate_web_pages_collapse_after_geography_and_category_filter():
    from backend.chat.processor import _filter_web_schemes
    from backend.models.schemas import ChatState, SchemeResult

    original = SchemeResult(
        scheme_name="National Old Age Pension Scheme (IGNOAPS)",
        details="Senior citizens receive an old age pension under the national scheme.",
        benefits="Monthly pension", eligibility="Senior citizens aged 60 or above.",
        application="https://one.gov.in", documents="", level="Central",
        schemeCategory="Social welfare", tags="Senior Citizen, Pension",
    )
    duplicate = original.model_copy(update={"scheme_name": "National Old Age Pension Scheme", "application": "https://two.gov.in"})
    state = ChatState(collected_facts={"state": "Karnataka"}, target_group_context="senior_citizen")
    filtered = _filter_web_schemes([original, duplicate], "senior citizen pension Karnataka", state)
    assert len(filtered) == 1
