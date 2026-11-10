from backend.chat.intent import detect_intent


def test_detects_eligibility_and_section():
    result = detect_intent("Am I eligible for this scheme?")
    assert result.to_dict() == {
        "intent": "check_eligibility",
        "confidence": 0.9,
        "scheme_name": None,
        "requested_section": "eligibility",
    }


def test_detects_known_scheme_without_guessing_name():
    assert detect_intent("tell me about a scheme", ["PM Kisan"]).scheme_name is None
    result = detect_intent("benefits of PM Kisan", ["PM Kisan"])
    assert result.scheme_name == "PM Kisan"
    assert result.intent == "benefits"


def test_detects_followup_and_unknown():
    assert detect_intent("yes").intent == "follow_up"
    assert detect_intent("hello there").intent == "greeting"


def test_detects_other_intents():
    assert detect_intent("compare PM Kisan and another scheme").intent == "compare_schemes"
    assert detect_intent("track my application status").intent == "application_status"
    assert detect_intent("show me schemes for farmers").intent == "find_scheme"
