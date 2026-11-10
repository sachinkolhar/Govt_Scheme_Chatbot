from backend.chat.clarification import accept_clarification_reply, begin_clarification, confidence_band
from backend.models.schemas import ChatState


def test_confidence_bands_use_configured_thresholds():
    assert confidence_band(0.9) == "HIGH_CONFIDENCE"
    assert confidence_band(0.6) == "MEDIUM_CONFIDENCE"
    assert confidence_band(0.1) == "LOW_CONFIDENCE"


def test_clarification_preserves_query_candidates_and_collects_state():
    state = ChatState()
    question = begin_clarification(state, "find schemes for me", ["state", "income"], [{"name": "candidate"}])
    assert question == "Which state do you live in?"
    result = accept_clarification_reply(state, "Karnataka")
    assert result["original_query"] == "find schemes for me"
    assert result["facts"]["state"] == "Karnataka"
    assert result["previous_candidates"] == [{"name": "candidate"}]
    assert result["pending_question"] is None


def test_unparsed_reply_keeps_clarification_pending():
    state = ChatState()
    begin_clarification(state, "find schemes", ["state"])
    result = accept_clarification_reply(state, "not sure")
    assert result["required_field"] == "state"
    assert result["pending_question"] == "Which state do you live in?"
