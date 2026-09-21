"""
Text processing utilities for NLP operations.
"""
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def _load_stop_words() -> set[str]:
    """Load stopwords without triggering network access during import."""
    try:
        return set(stopwords.words("english"))
    except LookupError:
        return set()


stop_words = _load_stop_words()


def _safe_lemmatize(token: str) -> str:
    try:
        return lemmatizer.lemmatize(token)
    except LookupError:
        return token


def clean_text(text: str) -> str:
    """
    Clean and normalize text by:
    - Converting to lowercase
    - Removing special characters
    - Removing stopwords
    - Lemmatizing tokens
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned and normalized text
    """
    text = (text or "").lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = [t for t in text.split() if t and t not in stop_words]
    return " ".join(_safe_lemmatize(t) for t in tokens)
