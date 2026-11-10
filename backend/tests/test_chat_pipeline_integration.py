import pandas as pd
import pytest
from fastapi.testclient import TestClient

import backend.main as main
import backend.search.semantic as semantic
from backend.voice.processor import process_voice_assistant_chat
from backend.models.schemas import VoiceAssistantChatRequest
from backend.chat.processor import stream_chat_events


@pytest.fixture
def pipeline_data(monkeypatch):
    frame = pd.DataFrame([
        {
            "scheme_name": "PM Kisan",
            "details": "Central income support for eligible farmer families.",
            "benefits": "Eligible landholder farmer families receive income support.",
            "eligibility": "Small and marginal farmer families owning cultivable land may apply.",
            "application": "Apply through the official PM Kisan portal or local agriculture office.",
            "documents": "Aadhaar and land records.",
            "level": "Central", "schemeCategory": "Agriculture", "tags": "farmer kisan",
        },
        {
            "scheme_name": "Student Scholarship",
            "details": "Education assistance for eligible students.",
            "benefits": "Scholarship support for students.",
            "eligibility": "Students enrolled in an eligible course may apply.",
            "application": "Apply through the scholarship portal.",
            "documents": "Proof of enrollment and income certificate.",
            "level": "Central", "schemeCategory": "Education", "tags": "student scholarship",
        },
        {
            "scheme_name": "Karnataka Farmer Support",
            "details": "State agriculture support for Karnataka residents.",
            "benefits": "Agriculture support for eligible Karnataka farmers.",
            "eligibility": "Karnataka resident farmers may apply.",
            "application": "Apply through the Karnataka agriculture office.",
            "documents": "Identity and land records.",
            "level": "Karnataka State", "schemeCategory": "Agriculture", "tags": "farmer karnataka",
        },
    ])
    monkeypatch.setattr(semantic, "df", frame)
    monkeypatch.setattr(main, "semantic_candidates", lambda _query, _k: [(0, 0.05), (1, 0.1), (2, 0.15)])
    monkeypatch.setattr(main, "generate_answer_with_groq", lambda query, _scheme, _history=None: f"Grounded answer for {query}")
    main.chat_state_store.clear()
    return frame


def test_a_explicit_facts_flow_through_shared_pipeline(pipeline_data):
    response = main.chat(main.ChatRequest(
        query="I am a 24 year old student from Karnataka with family income of two lakh. What schemes can I get?",
        conversation_id="scenario-a",
    ))
    assert response.response_type == "direct_answer"
    assert response.source_scheme is not None
    assert len(response.relevant_schemes) <= 5
    assert all(item.scheme_name != "PM Kisan" for item in response.relevant_schemes)


def test_b_farmer_discovery_uses_state_and_farmer_facts(pipeline_data):
    response = main.chat(main.ChatRequest(
        query="I am a farmer from Karnataka. What schemes are available?",
        conversation_id="scenario-b",
    ))
    assert response.response_type == "direct_answer"
    names = {item.scheme_name for item in response.relevant_schemes}
    assert "Karnataka Farmer Support" in names
    assert "PM Kisan" in names


def test_c_explicit_scheme_eligibility_prioritizes_named_scheme(pipeline_data):
    response = main.chat(main.ChatRequest(query="Can I get PM Kisan?", conversation_id="scenario-c"))
    assert response.response_type == "clarification"
    assert response.source_scheme is None
    assert "occupation" in response.answer.lower() or "farmer" in response.answer.lower()


def test_d_to_f_section_followups_keep_scheme_context(pipeline_data):
    first = main.chat(main.ChatRequest(query="What are the benefits of PM Kisan?", conversation_id="scenario-d"))
    assert "Benefits" in first.answer
    docs = main.chat(main.ChatRequest(query="What documents do I need?", conversation_id="scenario-d"))
    assert "PM Kisan" in docs.answer
    assert "Aadhaar and land records" in docs.answer
    application = main.chat(main.ChatRequest(query="How do I apply?", conversation_id="scenario-d"))
    assert "official PM Kisan portal" in application.answer


def test_g_broad_ambiguous_discovery_asks_one_missing_state(pipeline_data):
    response = main.chat(main.ChatRequest(query="What schemes can I get?", conversation_id="scenario-g"))
    assert response.response_type == "clarification"
    assert response.answer == "Which state do you live in?"


def test_h_low_confidence_does_not_recommend(monkeypatch, pipeline_data):
    monkeypatch.setattr(main, "semantic_candidates", lambda _query, _k: [(0, 100.0)])
    response = main.chat(main.ChatRequest(query="unknown query", conversation_id="scenario-h"))
    assert response.response_type == "no_data_prompt"
    assert response.source_scheme is None


def test_i_state_answer_resumes_original_query(pipeline_data):
    first = main.chat(main.ChatRequest(query="What schemes can I get?", conversation_id="scenario-i"))
    assert first.response_type == "clarification"
    second = main.chat(main.ChatRequest(query="Karnataka", conversation_id="scenario-i"))
    assert second.response_type == "direct_answer"
    assert second.source_scheme is not None


def test_j_voice_uses_same_grounded_chat_pipeline(pipeline_data):
    response = process_voice_assistant_chat(VoiceAssistantChatRequest(
        query="I am a farmer from Karnataka. What schemes are available?",
        conversation_id="scenario-j",
    ))
    assert response.answer
    assert "PM Kisan" not in response.answer  # voice formatter returns the mocked concise answer
    assert response.answer.startswith("Grounded answer")


def test_streaming_chat_uses_shared_pipeline_and_clarification(pipeline_data):
    events = "".join(stream_chat_events(main.ChatRequest(
        query="What schemes can I get?", conversation_id="scenario-stream",
    )))
    assert '"value": "clarification"' in events
    assert "Which state do you live in?" in events


def test_chat_and_stream_http_endpoints_return_compatible_events(pipeline_data):
    client = TestClient(main.app)
    request = {
        "query": "Tell me about PM Kisan",
        "conversation_id": "http-chat-smoke",
        "top_k": 5,
        "language": "en",
    }
    response = client.post("/api/chat", json=request)
    assert response.status_code == 200
    assert response.json()["source_scheme"]["scheme_name"] == "PM Kisan"

    streamed = client.post("/api/chat/stream", json={**request, "conversation_id": "http-stream-smoke"})
    assert streamed.status_code == 200
    assert '"type": "token"' in streamed.text
    assert '"type": "done"' in streamed.text


def test_second_recent_scheme_followup_resolves_correct_candidate(pipeline_data):
    first = main.chat(main.ChatRequest(query="I live in Karnataka; what schemes are available?", conversation_id="ordinal"))
    expected = first.relevant_schemes[1].scheme_name
    response = main.chat(main.ChatRequest(query="Tell me about the second scheme", conversation_id="ordinal"))
    assert response.source_scheme is not None
    assert response.source_scheme.scheme_name == expected


def test_ambiguous_this_one_followup_asks_user_to_choose(pipeline_data):
    main.chat(main.ChatRequest(query="I live in Karnataka; what schemes are available?", conversation_id="ambiguous"))
    response = main.chat(main.ChatRequest(query="What about this one?", conversation_id="ambiguous"))
    assert response.response_type == "clarification"
    assert "Which scheme do you mean" in response.answer


def test_hindi_ignoaps_query_selects_central_record_and_answers_in_hindi(monkeypatch):
    frame = pd.DataFrame([
        {
            "scheme_name": "NSAP - Indira Gandhi National Old Age Pension Scheme",
            "details": "Central old age pension scheme.",
            "benefits": "Pension support.",
            "eligibility": "As recorded in the central scheme data.",
            "application": "Apply through the listed government process.",
            "documents": "See the listed documents.",
            "level": "Central", "schemeCategory": "Social welfare", "tags": "old age pension",
        },
        {
            "scheme_name": "Swavalambi/Sanchari Marata Malige",
            "details": "Karnataka-specific unrelated scheme.",
            "benefits": "Karnataka support.",
            "eligibility": "Karnataka residents.",
            "application": "Apply in Karnataka.",
            "documents": "Identity proof.",
            "level": "Karnataka State", "schemeCategory": "Business", "tags": "Karnataka",
        },
    ])
    monkeypatch.setattr(semantic, "df", frame)
    monkeypatch.setattr(main, "semantic_candidates", lambda _query, _k: [(0, 0.05), (1, 0.01)])
    generated_queries = []

    def answer(query, _scheme, _history=None):
        generated_queries.append(query)
        return "यह केंद्रीय वृद्धावस्था पेंशन योजना है।"

    monkeypatch.setattr(main, "generate_answer_with_groq", answer)
    main.chat_state_store.clear()
    response = main.chat(main.ChatRequest(
        query="इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना के बारे में बताइए।",
        language="hi",
        conversation_id="hindi-ignoaps",
    ))
    assert response.response_type == "direct_answer"
    assert response.source_scheme.scheme_name == "NSAP - Indira Gandhi National Old Age Pension Scheme"
    assert all(item.scheme_name != "Swavalambi/Sanchari Marata Malige" for item in response.relevant_schemes)
    assert response.answer == "यह केंद्रीय वृद्धावस्था पेंशन योजना है।"
    assert "Please answer in Hindi." in generated_queries[0]
    assert "इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना" in generated_queries[0]


def test_legacy_hindi_language_prefix_does_not_pollute_retrieval_query():
    from backend.chat.query_normalization import normalize_query_for_retrieval

    assert normalize_query_for_retrieval(
        "Please answer in Hindi. Question: इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना के बारे में बताइए।"
    ) == "NSAP - Indira Gandhi National Old Age Pension Scheme के बारे में बताइए।"
