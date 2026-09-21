"""Speech-to-text processing."""
import base64
import os
import re
import shutil
import sys
import tempfile

try:
    import whisper as whisper_lib
except ImportError:
    whisper_lib = None

try:
    from ..models.schemas import SpeechRequest, SpeechResponse
    from ..utils.constants import SPEECH_LANGUAGE_MAP
    from ..utils.errors import format_speech_error, normalize_language_code
except ImportError:
    from models.schemas import SpeechRequest, SpeechResponse
    from utils.constants import SPEECH_LANGUAGE_MAP
    from utils.errors import format_speech_error, normalize_language_code


def _whisper_model():
    """Get the pre-loaded Whisper model from main module (loaded at startup)."""
    main_module = sys.modules.get("backend.main") or sys.modules.get("main")
    if main_module is not None and hasattr(main_module, "whisper_model"):
        return getattr(main_module, "whisper_model")
    # Fallback: load model if not pre-loaded
    try:
        import whisper as whisper_lib
        if whisper_lib is not None:
            return whisper_lib.load_model("small", device="cpu")
    except Exception:
        pass
    return None


def _audio_extension(audio_format: str) -> str:
    """Return a safe file extension for ffmpeg-backed Whisper decoding."""
    normalized = re.sub(r"[^a-z0-9]", "", (audio_format or "").lower())
    supported = {
        "wav": "wav",
        "wave": "wav",
        "mp3": "mp3",
        "mpeg": "mp3",
        "ogg": "ogg",
        "oga": "ogg",
        "webm": "webm",
        "m4a": "m4a",
        "mp4": "mp4",
        "flac": "flac",
    }
    return supported.get(normalized, "webm")


def transcribe_audio(payload: SpeechRequest) -> SpeechResponse:
    """Convert audio (base64-encoded) to text using Whisper STT."""
    try:
        if not payload.audio_base64:
            raise ValueError("No audio data provided")

        language = normalize_language_code(payload.language)

        raw_audio = payload.audio_base64
        if "," in raw_audio:
            raw_audio = raw_audio.split(",", 1)[1]

        try:
            audio_bytes = base64.b64decode(raw_audio, validate=True)
        except Exception as exc:
            raise ValueError(f"Invalid base64 audio: {str(exc)}") from exc

        if len(audio_bytes) == 0:
            raise ValueError("Audio data is empty")

        audio_ext = _audio_extension(payload.format)
        with tempfile.NamedTemporaryFile(suffix=f".{audio_ext}", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            model = _whisper_model()
            if model is None:
                raise ValueError("Whisper model not available. Speech recognition service is offline. Please try again later.")
            if shutil.which("ffmpeg") is None:
                raise ValueError("FFmpeg is required for Whisper speech recognition but was not found on PATH.")
            
            result = model.transcribe(
                tmp_path,
                language=SPEECH_LANGUAGE_MAP.get(language, "en"),
                fp16=False,  # Disable FP16 for CPU compatibility
                temperature=0,  # Single pass for speed
                condition_on_previous_text=False,
                verbose=False,  # Suppress debug output
            )
            transcribed_text = result.get("text", "").strip()

            if not transcribed_text:
                raise ValueError("No speech detected in audio")

            return SpeechResponse(
                success=True,
                data=transcribed_text,
                language=language,
            )
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as exc:
        return SpeechResponse(
            success=False,
            data=None,
            error=format_speech_error(str(exc), payload.language),
            language=normalize_language_code(payload.language),
        )
