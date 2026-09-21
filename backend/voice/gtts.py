"""Text-to-speech processing."""
import base64
import os
import sys
import tempfile

try:
    from gtts import gTTS as gtts_class
except ImportError:
    gtts_class = None

try:
    from ..models.schemas import SpeechRequest, SpeechResponse
    from ..utils.constants import TTS_LANGUAGE_MAP
    from ..utils.errors import format_speech_error, normalize_language_code
except ImportError:
    from models.schemas import SpeechRequest, SpeechResponse
    from utils.constants import TTS_LANGUAGE_MAP
    from utils.errors import format_speech_error, normalize_language_code


def _gtts_class():
    main_module = sys.modules.get("backend.main") or sys.modules.get("main")
    if main_module is not None and hasattr(main_module, "gTTS"):
        return getattr(main_module, "gTTS")
    return gtts_class


def synthesize_audio(payload: SpeechRequest) -> SpeechResponse:
    """Convert text to speech (base64-encoded audio) using gTTS."""
    try:
        if not payload.text or not payload.text.strip():
            raise ValueError("No text provided for synthesis")

        language = normalize_language_code(payload.language)
        tts_lang = TTS_LANGUAGE_MAP.get(language, "en")
        gtts = _gtts_class()

        if gtts is None:
            raise RuntimeError("gTTS is not installed on the backend")
        else:
            tts = gtts(text=payload.text, lang=tts_lang, slow=False)

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp_path = tmp.name

            try:
                tts.save(tmp_path)
                with open(tmp_path, "rb") as f:
                    audio_bytes = f.read()
                if not audio_bytes:
                    raise RuntimeError("gTTS returned empty audio")
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        return SpeechResponse(
            success=True,
            data=audio_base64,
            language=language,
        )

    except Exception as exc:
        return SpeechResponse(
            success=False,
            data=None,
            error=format_speech_error(str(exc), payload.language),
            language=normalize_language_code(payload.language),
        )
