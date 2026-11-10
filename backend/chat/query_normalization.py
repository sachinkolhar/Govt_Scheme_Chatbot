"""Deterministic query normalization for named schemes in supported languages."""
import re


_LANGUAGE_PREFIX = re.compile(
    r"^\s*please\s+answer\s+in\s+(?:hindi|english|telugu|tamil)\s*[.!]?\s*question\s*:\s*",
    re.IGNORECASE,
)

_HINDI_SCHEME_NAMES = {
    "इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना":
        "NSAP - Indira Gandhi National Old Age Pension Scheme",
}


def normalize_query_for_retrieval(query: str) -> str:
    """Remove legacy language wrappers and normalize known Hindi scheme names."""
    normalized = _LANGUAGE_PREFIX.sub("", str(query or "")).strip()
    for hindi_name, dataset_name in _HINDI_SCHEME_NAMES.items():
        normalized = normalized.replace(hindi_name, dataset_name)
    return normalized


def query_for_answer_language(query: str, language: str) -> str:
    """Keep language preference in the generation prompt, outside retrieval."""
    normalized_query = _LANGUAGE_PREFIX.sub("", str(query or "")).strip()
    language_name = {"hi": "Hindi", "te": "Telugu", "ta": "Tamil"}.get(
        str(language or "en").lower(), "English"
    )
    if language_name == "English":
        return normalized_query
    return f"Please answer in {language_name}. Question: {normalized_query}"
