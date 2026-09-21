"""IVR API routes for translation and speech."""
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

try:
    from groq import Groq
except ImportError:
    Groq = None

# Ensure backend directory is in sys.path for reliable imports
_backend_dir = str(Path(__file__).parent.parent)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

try:
    from voice.gtts import synthesize_audio
    from config.settings import GROQ_API_KEY, GROQ_MODEL
    from models.schemas import SpeechRequest, SpeechResponse
except ImportError as e:
    raise ImportError(f"Failed to import IVR dependencies from {_backend_dir}: {e}") from e

from .schemes import DEMO_SCHEMES, LANGUAGE_MAP, LANGUAGE_NAMES

router = APIRouter(prefix="/api/ivr", tags=["ivr"])


class TranslateRequest(BaseModel):
    text: str
    language: str


class SpeakRequest(BaseModel):
    text: str
    language: str


class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    language: str


class SpeakResponse(BaseModel):
    audio: str = ""  # base64-encoded audio data
    language: str
    text: str
    format: str
    success: bool = True
    error: str | None = None



@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """Translate text to specified language using Groq."""
    try:
        language = request.language.lower()
        
        # If already in English, no translation needed
        if language == "english":
            return TranslateResponse(
                original_text=request.text,
                translated_text=request.text,
                language="English",
            )
        
        # Map language codes to language names
        language_full = {
            "kannada": "Kannada",
            "hindi": "Hindi",
            "telugu": "Telugu",
            "tamil": "Tamil",
        }.get(language, language)
        
        # Use Groq to translate
        if not Groq or not GROQ_API_KEY:
            raise ValueError("Groq API not configured")
        
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following text to {language_full}. Return ONLY the translated text, nothing else:\n\n{request.text}",
                }
            ],
        )
        
        translated = completion.choices[0].message.content.strip()
        
        return TranslateResponse(
            original_text=request.text,
            translated_text=translated,
            language=language_full,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.post("/speak", response_model=SpeakResponse)
async def speak_text(request: SpeakRequest):
    """Generate speech from text using TTS."""
    try:
        # Map language to language code for TTS
        language_code = {
            "english": "en",
            "kannada": "kn",
            "hindi": "hi",
            "telugu": "te",
            "tamil": "ta",
        }.get(request.language.lower(), "en")
        
        # Create speech request
        speech_req = SpeechRequest(
            text=request.text,
            language=language_code
        )
        
        # Generate speech using existing TTS system
        response = synthesize_audio(speech_req)
        
        if not response.success:
            return SpeakResponse(
                audio="",
                language=request.language,
                text=request.text,
                format="mp3",
                success=False,
                error=response.error or "Speech synthesis failed",
            )
        
        return SpeakResponse(
            audio=response.data,  # base64-encoded audio
            language=request.language,
            text=request.text,
            format="mp3",
            success=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech generation failed: {str(e)}")


@router.get("/scheme/demo")
async def get_demo_scheme():
    """Get hardcoded PM Kisan demo scheme data."""
    return DEMO_SCHEMES.get("pm_kisan")


@router.get("/languages")
async def get_languages():
    """Get available languages for IVR demo."""
    return {
        "1": "English",
        "2": "Kannada",
        "3": "Hindi",
        "4": "Telugu",
        "5": "Tamil",
        "6": "Exit",
    }
