"""Voice and audio API routes."""
from fastapi import APIRouter

try:
    from ..models.schemas import (
        SpeechRequest,
        SpeechResponse,
        VoiceAssistantChatRequest,
        VoiceAssistantChatResponse,
        VoiceEligibilityCriteriaRequest,
        VoiceEligibilityCriteriaResponse,
    )
    from .gtts import synthesize_audio
    from .processor import (
        process_voice_assistant_chat,
        process_voice_eligibility_criteria,
    )
    from .whisper import transcribe_audio
except ImportError:
    from models.schemas import (
        SpeechRequest,
        SpeechResponse,
        VoiceAssistantChatRequest,
        VoiceAssistantChatResponse,
        VoiceEligibilityCriteriaRequest,
        VoiceEligibilityCriteriaResponse,
    )
    from voice.gtts import synthesize_audio
    from voice.processor import (
        process_voice_assistant_chat,
        process_voice_eligibility_criteria,
    )
    from voice.whisper import transcribe_audio


router = APIRouter(prefix="/api", tags=["voice"])


@router.post("/audio/transcribe", response_model=SpeechResponse)
def transcribe_audio_route(payload: SpeechRequest) -> SpeechResponse:
    return transcribe_audio(payload)


@router.post("/audio/synthesize", response_model=SpeechResponse)
def synthesize_audio_route(payload: SpeechRequest) -> SpeechResponse:
    return synthesize_audio(payload)


@router.post("/voice-assistant/chat", response_model=VoiceAssistantChatResponse)
def voice_assistant_chat(
    payload: VoiceAssistantChatRequest,
) -> VoiceAssistantChatResponse:
    return process_voice_assistant_chat(payload)


@router.post(
    "/voice-assistant/eligibility-criteria",
    response_model=VoiceEligibilityCriteriaResponse,
)
def voice_eligibility_criteria(
    payload: VoiceEligibilityCriteriaRequest,
) -> VoiceEligibilityCriteriaResponse:
    return process_voice_eligibility_criteria(payload)
