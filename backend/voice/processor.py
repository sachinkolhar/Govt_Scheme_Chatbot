"""Voice assistant request processing."""
from fastapi import HTTPException

try:
    from ..chat.groq_client import (
        generate_voice_assistant_answer_with_groq,
        get_voice_eligibility_criteria_with_groq,
    )
    from ..models.schemas import (
        VoiceAssistantChatRequest,
        VoiceAssistantChatResponse,
        VoiceEligibilityCriteriaRequest,
        VoiceEligibilityCriteriaResponse,
    )
    from ..utils.errors import normalize_language_code
except ImportError:
    from chat.groq_client import (
        generate_voice_assistant_answer_with_groq,
        get_voice_eligibility_criteria_with_groq,
    )
    from models.schemas import (
        VoiceAssistantChatRequest,
        VoiceAssistantChatResponse,
        VoiceEligibilityCriteriaRequest,
        VoiceEligibilityCriteriaResponse,
    )
    from utils.errors import normalize_language_code


def process_voice_assistant_chat(
    payload: VoiceAssistantChatRequest,
) -> VoiceAssistantChatResponse:
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    language = normalize_language_code(payload.language)
    answer = generate_voice_assistant_answer_with_groq(
        query=query,
        language=language,
        history=payload.history,
    )

    return VoiceAssistantChatResponse(
        query=query,
        answer=answer,
        language=language,
    )


def process_voice_eligibility_criteria(
    payload: VoiceEligibilityCriteriaRequest,
) -> VoiceEligibilityCriteriaResponse:
    scheme_name = payload.scheme_name.strip()
    if not scheme_name:
        raise HTTPException(status_code=400, detail="Scheme name cannot be empty")

    language = normalize_language_code(payload.language)
    criteria = get_voice_eligibility_criteria_with_groq(
        scheme_name=scheme_name,
        language=language,
    )

    return VoiceEligibilityCriteriaResponse(
        scheme_name=scheme_name,
        language=language,
        criteria=criteria,
    )
