"""
Error formatting utilities for consistent error messaging.
"""

try:
    from .constants import SPEECH_LANGUAGE_MAP
except ImportError:
    from utils.constants import SPEECH_LANGUAGE_MAP


def normalize_language_code(lang: str) -> str:
    """
    Normalize and validate language code, fallback to English if unsupported.
    
    Args:
        lang: Language code (e.g., 'en', 'hi', 'te', 'ta')
        
    Returns:
        Normalized language code or 'en' if unsupported
    """
    normalized = lang.strip().lower() if lang else "en"
    if normalized in SPEECH_LANGUAGE_MAP:
        return normalized
    return "en"


def format_speech_error(error: str, language: str = "en") -> str:
    """
    Format error message for speech operations with localization.
    
    Args:
        error: Error description
        language: Language code for localization
        
    Returns:
        Localized error message
    """
    error_messages = {
        "en": "Speech processing failed. Try again or use text input.",
        "hi": "भाषण प्रसंस्करण विफल। पुनः प्रयास करें या पाठ इनपुट का उपयोग करें।",
        "te": "ఆడియో ప్రక్రియ విఫలమైంది. మళ్లీ ప్రయత్నించండి లేదా టెక్స్ట్ ఇన్‌పుట్‌ను ఉపయోగించండి.",
        "ta": "பேச்சு செயலாக்கம் தோல்வியடைந்தது. மீண்டும் முயற்சிக்கவும் அல்லது உரை உள்ளீட்டைப் பயன்படுத்தவும்.",
    }
    lang_normalized = normalize_language_code(language)
    if lang_normalized == "en" and "ffmpeg" in error.lower():
        return (
            "Speech processing failed. FFmpeg is missing on the backend. "
            "Install FFmpeg and add it to PATH, or use browser speech recognition."
        )
    return error_messages.get(lang_normalized, error_messages["en"])
