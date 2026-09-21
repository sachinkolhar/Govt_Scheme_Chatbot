"""
Constants used across the application.
"""

# ---- Language Support ----
SPEECH_LANGUAGE_MAP = {
    "en": "en",
    "kn": "kn",
    "hi": "hi",
    "te": "te",
    "ta": "ta",
}

# Language to gTTS language code mapping for TTS
TTS_LANGUAGE_MAP = {
    "en": "en",
    "kn": "kn",
    "hi": "hi",
    "te": "te",
    "ta": "ta",
}

# ---- Occupation Keywords ----
FARMER_KEYWORDS = [
    "farmer",
    "agriculture",
    "farm",
    "agricultural",
    "crop",
    "farming",
    "cultivate",
]

STUDENT_KEYWORDS = [
    "student",
    "education",
    "school",
    "college",
    "university",
    "scholar",
    "studying",
]

DISABILITY_KEYWORDS = [
    "disability",
    "disable",
    "disabled",
    "handicap",
    "impaired",
    "physically challenged",
    "pwd",
]

# ---- Gender Variations ----
GENDER_MALE = ["male", "boy", "man", "m", "mr", "sir"]
GENDER_FEMALE = ["female", "girl", "woman", "f", "mrs", "ms", "madam"]

# ---- Income Categories ----
INCOME_UPPER_LIMITS = {
    "general": 1000000,
    "obc": 1000000,
    "sc": 1000000,
    "st": 1000000,
}

# ---- Age Limits ----
AGE_SENIOR_CITIZEN = 60
AGE_SENIOR_CITIZEN_WOMAN = 55

# ---- Scheme Categories ----
SCHEME_CATEGORIES = [
    "Education",
    "Health",
    "Employment",
    "Agriculture",
    "Social Welfare",
    "Women Welfare",
    "Housing",
    "Disability",
]

# ---- API Response Types ----
RESPONSE_DIRECT_ANSWER = "direct_answer"
RESPONSE_NO_DATA = "no_data_prompt"
RESPONSE_RELEVANT_SCHEMES = "relevant_schemes"
