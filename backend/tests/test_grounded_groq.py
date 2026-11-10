from types import SimpleNamespace

import pandas as pd

import backend.chat.groq_client as groq_client
from backend.chat.groq_client import build_voice_assistant_messages


def test_section_context_contains_only_requested_section():
    scheme = pd.Series({
        "scheme_name": "Test Scheme", "benefits": "Monthly support", "eligibility": "Age 18+",
        "application": "Apply online", "documents": "ID proof", "details": "A test",
    })
    messages = groq_client.build_groq_messages("What are the benefits?", [], groq_client.build_scheme_context(scheme))
    content = messages[-1]["content"]
    assert "Monthly support" in content
    assert "Age 18+" not in content
    assert "Apply online" not in content


def test_prompt_forbids_general_knowledge_and_claims_without_data():
    assert "Do not use general knowledge" in groq_client._GROQ_SYSTEM_PROMPT
    content = groq_client.build_groq_messages("What is the deadline?", [], None)[-1]["content"]
    assert "No retrieved scheme data" in content


def test_voice_scheme_prompt_requires_retrieved_data_but_allows_non_scheme_help():
    content = build_voice_assistant_messages("Can I get PM Kisan?", "en", [])[0]["content"]
    assert "retrieved scheme information only" in content
    assert "explicitly say" in content
    assert "do not use general knowledge" in content
    assert "For non-scheme questions, answer normally" in content


def test_generate_answer_uses_retrieved_data_with_mocked_groq(monkeypatch):
    captured = {}

    class FakeGroq:
        def __init__(self, api_key):
            captured["api_key"] = api_key
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

        def create(self, **kwargs):
            captured.update(kwargs)
            message = SimpleNamespace(content="The supplied data says monthly support.")
            return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    monkeypatch.setattr(groq_client, "GROQ_API_KEY", "test-key")
    monkeypatch.setitem(__import__("sys").modules, "groq", SimpleNamespace(Groq=FakeGroq))
    scheme = pd.Series({"scheme_name": "Test", "benefits": "Monthly support", "eligibility": "Age 18+"})
    answer = groq_client.generate_answer_with_groq("What are the benefits?", scheme)
    assert answer == "The supplied data says monthly support."
    assert "Monthly support" in captured["messages"][-1]["content"]
    assert "Age 18+" not in captured["messages"][-1]["content"]
