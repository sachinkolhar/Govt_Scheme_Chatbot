import pandas as pd

import backend.main as main
import backend.search.semantic as semantic
from backend.chat.intent import detect_intent, detect_target_group
from backend.chat.state import get_chat_state
from backend.search.geography import is_geographically_applicable
from backend.search.ranking import category_relevance, rank_candidates


def _actual_row(name):
    data = pd.read_csv("dataset/govt_schemes.csv")
    return data.loc[data.scheme_name.eq(name)].iloc[0]


def test_target_group_extraction_uses_existing_intent_representation():
    intent = detect_intent("senior citizen pension scheme")
    assert intent.intent == "find_scheme"
    assert intent.target_group == "senior_citizen"
    assert detect_target_group("construction worker pension scheme") == "construction_worker"
    assert detect_target_group("farmer pension scheme") == "farmer"


def test_real_karnataka_construction_worker_pension_is_not_senior_citizen_match():
    kbocwwb = _actual_row("Pension Scheme (K.B.O.C.W.W.B)")
    assert "construction worker" in kbocwwb.details.lower()
    assert "senior citizen" in kbocwwb.tags.lower()  # metadata alone is not enough
    assert category_relevance(kbocwwb, "senior_citizen") == "NO_MATCH"
    assert category_relevance(kbocwwb, "construction_worker") == "MATCH"


def test_actual_old_age_scheme_outranks_semantically_closer_worker_pension():
    kbocwwb = _actual_row("Pension Scheme (K.B.O.C.W.W.B)")
    central_old_age = _actual_row("NSAP - Indira Gandhi National Old Age Pension Scheme")
    assert category_relevance(central_old_age, "senior_citizen") == "MATCH"
    candidates = rank_candidates(
        [(kbocwwb, 0.01), (central_old_age, 0.8)],
        profile={"state": "Karnataka"},
        query="senior citizen pension scheme Karnataka",
        target_group="senior_citizen",
        limit=2,
    )
    assert candidates[0].scheme.scheme_name == central_old_age.scheme_name
    assert candidates[0].category_relevance == "MATCH"


def test_real_farmer_pension_is_relevant_to_farmer_query():
    farmer_pension = _actual_row("Suraksha Laghu Evan Simant Vriddhajan Krishak Samman Pension Yojana")
    assert category_relevance(farmer_pension, "farmer") == "MATCH"
    assert category_relevance(farmer_pension, "senior_citizen") == "MATCH"


def test_unknown_target_group_evidence_cannot_be_high_confidence(monkeypatch):
    actual = _actual_row("Incentive For The Intra Caste Marriage within Scheduled Tribe Community")
    frame = pd.DataFrame([actual])
    monkeypatch.setattr(semantic, "df", frame)
    monkeypatch.setattr(main, "semantic_candidates", lambda _query, _k: [(0, 0.01)])
    main.chat_state_store.clear()
    response = main.chat(main.ChatRequest(
        query="senior citizen pension scheme Karnataka", conversation_id="unknown-target-group",
    ))
    assert category_relevance(actual, "senior_citizen") == "UNKNOWN"
    assert response.response_type == "no_data_prompt"
    assert response.source_scheme is None


def test_yes_fallback_reuses_geography_and_category_before_web(monkeypatch):
    kbocwwb = _actual_row("Pension Scheme (K.B.O.C.W.W.B)")
    dnh = _actual_row("Pension Scheme to Old Age Persons (Senior Citizen)")
    frame = pd.DataFrame([dnh, kbocwwb])
    monkeypatch.setattr(semantic, "df", frame)
    retrieval_queries = []

    def candidates(query, _top_k):
        retrieval_queries.append(query)
        return [(0, 0.03), (1, 0.05)]

    monkeypatch.setattr(main, "semantic_candidates", candidates)
    web_queries = []
    other_state_web_result = main.SchemeResult(
        scheme_name="Kerala old age pension", details="Kerala residents receive an old age pension.",
        benefits="Monthly pension", eligibility="Senior citizens residing in Kerala.",
        application="https://example.gov.in", documents="identity proof", level="State",
        schemeCategory="Social welfare", tags="Senior Citizen, Pension",
    )
    wrong_category_web_result = main.SchemeResult(
        scheme_name="Karnataka construction worker pension", details="Karnataka registered construction workers receive pension.",
        benefits="Monthly pension", eligibility="Registered construction workers in Karnataka who have completed 60 years.",
        application="https://example.gov.in", documents="identity proof", level="State",
        schemeCategory="Social welfare", tags="Senior Citizen, Construction Worker, Pension",
    )

    def web_search(query, limit=5):
        web_queries.append(query)
        return [other_state_web_result, wrong_category_web_result][:limit]

    monkeypatch.setattr(main, "web_search_relevant_schemes", web_search)
    main.chat_state_store.clear()
    first = main.chat(main.ChatRequest(
        query="senior citizen pension scheme", conversation_id="yes-category-constraints",
    ))
    assert first.response_type == "clarification"
    second = main.chat(main.ChatRequest(query="Karnataka", conversation_id="yes-category-constraints"))
    assert second.response_type == "no_data_prompt"
    state = get_chat_state("yes-category-constraints")
    assert state.collected_facts["state"] == "Karnataka"
    assert state.target_group_context == "senior_citizen"
    yes = main.chat(main.ChatRequest(query="yes", conversation_id="yes-category-constraints"))
    assert yes.response_type == "direct_answer"
    assert yes.relevant_schemes == []
    assert all("senior citizen pension scheme" in query.lower() and "karnataka" in query.lower() for query in retrieval_queries[1:])
    assert len(web_queries) == 1
    assert "senior citizen pension" in web_queries[0].lower()
    assert "karnataka" in web_queries[0].lower()
    assert "official government" in web_queries[0].lower()


def test_central_old_age_scheme_and_followup_keep_active_context(monkeypatch):
    kbocwwb = _actual_row("Pension Scheme (K.B.O.C.W.W.B)")
    central_old_age = _actual_row("NSAP - Indira Gandhi National Old Age Pension Scheme")
    frame = pd.DataFrame([kbocwwb, central_old_age])
    monkeypatch.setattr(semantic, "df", frame)
    monkeypatch.setattr(main, "semantic_candidates", lambda _query, _k: [(0, 0.01), (1, 0.6)])
    main.chat_state_store.clear()
    first = main.chat(main.ChatRequest(
        query="senior citizen pension scheme", conversation_id="central-senior-followup",
    ))
    assert first.response_type == "clarification"
    second = main.chat(main.ChatRequest(query="Karnataka", conversation_id="central-senior-followup"))
    assert second.response_type == "direct_answer"
    assert second.source_scheme.scheme_name == central_old_age.scheme_name
    assert all(is_geographically_applicable(item.model_dump(), "Karnataka") for item in second.relevant_schemes)
    state = get_chat_state("central-senior-followup")
    assert state.collected_facts["state"] == "Karnataka"
    assert state.target_group_context == "senior_citizen"
    documents = main.chat(main.ChatRequest(query="What documents are required?", conversation_id="central-senior-followup"))
    assert documents.source_scheme.scheme_name == central_old_age.scheme_name
    assert get_chat_state("central-senior-followup").collected_facts["state"] == "Karnataka"
