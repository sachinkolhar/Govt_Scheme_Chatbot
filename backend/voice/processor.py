"""Voice assistant request processing."""
from fastapi import HTTPException
import re

try:
    from ..chat.groq_client import (
        get_voice_eligibility_criteria_with_groq,
    )
    from ..models.schemas import (
        ChatRequest,
        VoiceAssistantChatRequest,
        VoiceAssistantChatResponse,
        VoiceEligibilityCriteriaRequest,
        VoiceEligibilityCriteriaResponse,
    )
    from ..chat.processor import process_chat
    from ..utils.errors import normalize_language_code
except ImportError:
    from chat.groq_client import (
        get_voice_eligibility_criteria_with_groq,
    )
    from models.schemas import (
        ChatRequest,
        VoiceAssistantChatRequest,
        VoiceAssistantChatResponse,
        VoiceEligibilityCriteriaRequest,
        VoiceEligibilityCriteriaResponse,
    )
    from chat.processor import process_chat
    from utils.errors import normalize_language_code


def format_voice_response(text: str, max_chars: int = 420) -> str:
    """Remove speech-unfriendly markup and keep spoken replies short."""
    cleaned = re.sub(r"```.*?```", " ", text or "", flags=re.DOTALL)
    cleaned = re.sub(r"[`*_#]", "", cleaned)
    cleaned = re.sub(r"^\s*[-•]\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    questions = list(re.finditer(r"\?", cleaned))
    if len(questions) > 1:
        # Keep the first question only when the response contains several prompts.
        end = questions[0].end()
        later = cleaned[end:]
        if re.search(r"\b(what|which|where|when|how|are you|do you)\b", later, re.IGNORECASE):
            cleaned = cleaned[:end]
    if len(cleaned) > max_chars:
        shortened = cleaned[: max_chars - 1].rsplit(" ", 1)[0].rstrip(" ,;:")
        cleaned = shortened + "…"
    return cleaned


def process_voice_assistant_chat(
    payload: VoiceAssistantChatRequest,
) -> VoiceAssistantChatResponse:
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    language = normalize_language_code(payload.language)
    chat_response = process_chat(
        ChatRequest(
            query=query,
            language=language,
            history=payload.history,
            conversation_id=payload.conversation_id,
        )
    )
    answer = format_voice_response(chat_response.answer)

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
