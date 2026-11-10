import pandas as pd

import backend.main as main
import backend.search.semantic as semantic
from backend.chat.state import get_chat_state
from backend.search.geography import geographic_applicability, is_geographically_applicable


def _row(name, level, details="", eligibility=""):
    return pd.Series({
        "scheme_name": name, "level": level, "details": details,
        "eligibility": eligibility, "benefits": "", "application": "",
        "documents": "", "tags": "", "schemeCategory": "",
    })


def test_actual_dnh_old_age_scheme_is_rejected_for_karnataka():
    data = pd.read_csv("dataset/govt_schemes.csv")
    record = data.loc[data.scheme_name.eq("Pension Scheme to Old Age Persons (Senior Citizen)")].iloc[0]
    assert "Dadra & Nagar Haveli and Daman & Diu" in record.details
    assert geographic_applicability(record, "Karnataka") == "incompatible"


def test_actual_karnataka_pension_scheme_is_allowed_for_karnataka():
    data = pd.read_csv("dataset/govt_schemes.csv")
    record = data.loc[data.scheme_name.eq("Pension Scheme (K.B.O.C.W.W.B)")].iloc[0]
    assert geographic_applicability(record, "Karnataka") == "applicable"
    assert geographic_applicability(record, "Kerala") == "incompatible"


def test_state_constraint_keeps_central_and_rejects_unknown_and_other_states():
    assert is_geographically_applicable(_row("Central pension", "Central"), "Karnataka")
    assert is_geographically_applicable(_row("Karnataka pension", "State", "For residents of Karnataka"), "Karnataka")
    assert not is_geographically_applicable(_row("Kerala pension", "State", "For residents of Kerala"), "Karnataka")
    assert geographic_applicability(_row("State pension", "State"), "Karnataka") == "unknown"


def test_state_clarification_filters_actual_dnh_scheme_before_grounding(monkeypatch):
    data = pd.read_csv("dataset/govt_schemes.csv")
    dnh = data.loc[data.scheme_name.eq("Pension Scheme to Old Age Persons (Senior Citizen)")].iloc[0]
    frame = pd.DataFrame([dnh])
    monkeypatch.setattr(semantic, "df", frame)
    captured = []

    def candidates(query, top_k):
        captured.append((query, top_k))
        return [(0, 0.05)]

    monkeypatch.setattr(main, "semantic_candidates", candidates)
    main.chat_state_store.clear()
    first = main.chat(main.ChatRequest(query="senior citizen pension scheme", conversation_id="geo-dnh-regression"))
    assert first.response_type == "clarification"
    assert first.answer == "Which state do you live in?"

    second = main.chat(main.ChatRequest(query="karnataka", conversation_id="geo-dnh-regression"))
    chat_state = get_chat_state("geo-dnh-regression")
    assert chat_state.collected_facts["state"] == "Karnataka"
    assert "senior citizen pension scheme" in captured[-1][0]
    assert "Karnataka" in captured[-1][0]
    assert captured[-1][1] >= 20
    assert second.response_type == "no_data_prompt"
    assert second.source_scheme is None
    assert all("Dadra" not in item.scheme_name for item in second.relevant_schemes)


def test_state_answer_capitalization_is_normalized():
    from backend.models.schemas import ChatState
    from backend.chat.clarification import begin_clarification, accept_clarification_reply
    for answer in ("karnataka", "KARNATAKA", "Karnataka"):
        state = ChatState()
        begin_clarification(state, "senior citizen pension scheme", ["state"])
        assert accept_clarification_reply(state, answer)["facts"]["state"] == "Karnataka"


def test_web_fallback_query_retains_original_intent_and_state():
    from backend.models.schemas import ChatState
    from backend.chat.processor import _web_query_for_state
    state = ChatState(
        last_query="senior citizen pension scheme Karnataka",
        pending_original_query="senior citizen pension scheme Karnataka",
        collected_facts={"state": "Karnataka"},
    )
    query = _web_query_for_state(state, "yes")
    assert "senior citizen pension scheme" in query
    assert "Karnataka" in query
    assert "official government" in query
