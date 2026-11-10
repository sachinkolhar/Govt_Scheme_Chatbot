from backend.chat.facts import extract_user_facts


def test_extracts_supported_explicit_profile_facts_and_indian_income():
    facts = extract_user_facts("I am 24, a student from Karnataka and my family income is two lakh.")
    assert facts["age"] == 24
    assert facts["student_status"] is True
    assert facts["state"] == "Karnataka"
    assert facts["income"] == 200000


def test_income_units_and_explicit_supported_categories():
    facts = extract_user_facts("I am a farmer, male, OBC, earning 1.5 crore")
    assert facts["income"] == 15000000
    assert facts["farmer_status"] is True
    assert facts["gender"] == "male"
    assert facts["category"] == "OBC"


def test_contradictions_are_reported_and_saved_profile_is_not_overwritten():
    profile = {"age": 30, "state": "Tamil Nadu"}
    facts = extract_user_facts("I am 24 and live in Karnataka", profile)
    assert facts["age"] == 24
    assert facts["state"] == "Karnataka"
    assert set(facts["_conflicts"]) == {"age", "state"}
    assert profile == {"age": 30, "state": "Tamil Nadu"}


def test_conflicting_mentions_are_not_returned_as_fact():
    facts = extract_user_facts("I am 24 and 25")
    assert "age" not in facts
    assert "age" in facts["_conflicts"]


def test_uncertain_language_is_marked():
    assert extract_user_facts("Maybe I am a student") ["_uncertain"]
