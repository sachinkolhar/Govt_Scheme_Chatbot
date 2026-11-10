from backend.voice.processor import format_voice_response


def test_voice_formatter_removes_markdown_and_limits_length():
    formatted = format_voice_response("**Benefits**\n- Monthly support", max_chars=40)
    assert "**" not in formatted
    assert "- " not in formatted
    assert len(formatted) <= 40


def test_voice_formatter_keeps_at_most_one_clarifying_question():
    formatted = format_voice_response("I need more information. What is your age? Which state do you live in?")
    assert formatted.count("?") == 1


def test_voice_formatter_preserves_concise_plain_answer():
    assert format_voice_response("Your application status is not available in the retrieved records.") == "Your application status is not available in the retrieved records."
