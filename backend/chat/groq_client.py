"""Groq integration for chat answers."""
import json
import re
from typing import Optional

import pandas as pd

try:
    from ..config.settings import GROQ_API_KEY, GROQ_MODEL
    from ..models.schemas import ConversationMessage, VoiceEligibilityCriterion
    from ..utils.errors import normalize_language_code
except ImportError:
    from config.settings import GROQ_API_KEY, GROQ_MODEL
    from models.schemas import ConversationMessage, VoiceEligibilityCriterion
    from utils.errors import normalize_language_code


_GROQ_SYSTEM_PROMPT = (
    "You are a helpful AI assistant specializing in Indian government welfare schemes. "
    "Your job is to help Indian citizens understand government schemes, their benefits, "
    "eligibility criteria, and how to apply for them. "
    "When scheme data is provided, base your answer primarily on that data. "
    "When no specific scheme data is provided, answer from your general knowledge of "
    "Indian government schemes. Always be concise, accurate, and practical. "
    "Structure answers with labeled sections when helpful: **Summary**, **Eligibility**, "
    "**Benefits**, **How to Apply**. Use bullet points starting with '- ' for lists."
)


def build_scheme_context(scheme: pd.Series) -> str:
    return (
        f"Scheme Name: {str(scheme.get('scheme_name', ''))}\n"
        f"Details: {str(scheme.get('details', ''))}\n"
        f"Benefits: {str(scheme.get('benefits', ''))}\n"
        f"Eligibility: {str(scheme.get('eligibility', ''))}\n"
        f"How to Apply: {str(scheme.get('application', ''))}\n"
        f"Documents Required: {str(scheme.get('documents', ''))}\n"
        f"Level: {str(scheme.get('level', ''))}\n"
        f"Category: {str(scheme.get('schemeCategory', ''))}"
    )


def build_groq_messages(
    query: str,
    history: list[ConversationMessage],
    scheme_context: Optional[str] = None,
) -> list[dict]:
    messages: list[dict] = [{"role": "system", "content": _GROQ_SYSTEM_PROMPT}]
    for msg in history[-8:]:
        role = msg.role if msg.role in ("user", "assistant") else "user"
        messages.append({"role": role, "content": msg.content})
    user_content = (
        f"Use the following scheme information to answer:\n\n{scheme_context}\n\nQuestion: {query}"
        if scheme_context
        else query
    )
    messages.append({"role": "user", "content": user_content})
    return messages


def generate_answer_with_groq(
    query: str,
    scheme: pd.Series,
    history: Optional[list[ConversationMessage]] = None,
) -> str:
    scheme_name = str(scheme.get("scheme_name", "this scheme"))
    fallback = (
        f"Based on the retrieved scheme ({scheme_name}), here is what I found. "
        f"Eligibility: {str(scheme.get('eligibility', 'Not specified'))}. "
        f"Benefits: {str(scheme.get('benefits', 'Not specified'))}."
    )

    if not GROQ_API_KEY:
        return fallback

    try:
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)
        context = build_scheme_context(scheme)
        groq_messages = build_groq_messages(query, history or [], scheme_context=context)
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=groq_messages,
            temperature=0.2,
        )
        message = completion.choices[0].message.content if completion.choices else None
        if message and message.strip():
            return message.strip()
        return fallback
    except Exception:
        return fallback


def stream_answer_with_groq(
    query: str,
    history: list[ConversationMessage],
    scheme: pd.Series,
):
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)
    context = build_scheme_context(scheme)
    groq_messages = build_groq_messages(query, history, scheme_context=context)
    return client.chat.completions.create(
        model=GROQ_MODEL,
        messages=groq_messages,
        temperature=0.2,
        stream=True,
    )


def build_voice_assistant_messages(
    query: str,
    language: str,
    history: list[ConversationMessage],
) -> list[dict[str, str]]:
    language_map = {
        "en": "English",
        "hi": "Hindi",
        "te": "Telugu",
        "ta": "Tamil",
    }
    language_name = language_map.get(normalize_language_code(language), "English")

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a voice assistant focused on Indian government schemes. "
                "Answer only from general knowledge and user-provided context. "
                "Do not claim data was fetched from any local dataset. "
                "Keep answers concise, practical, and easy to understand."
            ),
        }
    ]
    for msg in history[-8:]:
        role = msg.role if msg.role in ("user", "assistant") else "user"
        messages.append({"role": role, "content": msg.content})
    messages.append(
        {
            "role": "user",
            "content": f"Respond in {language_name}. User question: {query}",
        }
    )
    return messages


def generate_voice_assistant_answer_with_groq(
    query: str,
    language: str,
    history: Optional[list[ConversationMessage]] = None,
) -> str:
    fallback_by_lang = {
        "en": "I am unable to answer right now. Please try again.",
        "hi": "मैं अभी उत्तर देने में असमर्थ हूँ। कृपया फिर से प्रयास करें।",
        "te": "నేను ఇప్పుడు సమాధానం ఇవ్వలేకపోతున్నాను. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "ta": "இப்போது பதிலளிக்க முடியவில்லை. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
    }
    normalized_language = normalize_language_code(language)
    fallback = fallback_by_lang.get(normalized_language, fallback_by_lang["en"])

    if not GROQ_API_KEY:
        return fallback

    try:
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=build_voice_assistant_messages(
                query=query,
                language=normalized_language,
                history=history or [],
            ),
            temperature=0.2,
        )
        message = completion.choices[0].message.content if completion.choices else None
        if message and message.strip():
            return message.strip()
        return fallback
    except Exception:
        return fallback


def default_voice_eligibility_criteria(
    scheme_name: str,
    language: str,
) -> list[VoiceEligibilityCriterion]:
    normalized_language = normalize_language_code(language)
    questions: dict[str, dict[str, tuple[str, str]]] = {
        "en": {
            "income": ("Annual income", "What is your annual family income?"),
            "category": ("Caste/category", "What is your caste or category?"),
            "qualification": ("Qualification", "What is your current academic qualification?"),
            "age": ("Age", "What is your age?"),
            "state": ("State/domicile", "Which state is your domicile or permanent residence?"),
        },
        "hi": {
            "income": ("वार्षिक आय", "आपके परिवार की वार्षिक आय कितनी है?"),
            "category": ("जाति/श्रेणी", "आपकी जाति या श्रेणी क्या है?"),
            "qualification": ("शैक्षणिक योग्यता", "आपकी वर्तमान शैक्षणिक योग्यता क्या है?"),
            "age": ("आयु", "आपकी उम्र कितनी है?"),
            "state": ("राज्य/निवास", "आपका डोमिसाइल या स्थायी निवास किस राज्य में है?"),
        },
        "te": {
            "income": ("వార్షిక ఆదాయం", "మీ కుటుంబ వార్షిక ఆదాయం ఎంత?"),
            "category": ("కులం/వర్గం", "మీ కులం లేదా వర్గం ఏమిటి?"),
            "qualification": ("విద్యార్హత", "మీ ప్రస్తుత విద్యార్హత ఏమిటి?"),
            "age": ("వయస్సు", "మీ వయస్సు ఎంత?"),
            "state": ("రాష్ట్రం/నివాసం", "మీ డొమిసైల్ లేదా శాశ్వత నివాస రాష్ట్రం ఏది?"),
        },
        "ta": {
            "income": ("ஆண்டு வருமானம்", "உங்கள் குடும்ப ஆண்டு வருமானம் எவ்வளவு?"),
            "category": ("சாதி/வகை", "உங்கள் சாதி அல்லது வகை என்ன?"),
            "qualification": ("கல்வித் தகுதி", "உங்கள் தற்போதைய கல்வித் தகுதி என்ன?"),
            "age": ("வயது", "உங்கள் வயது என்ன?"),
            "state": ("மாநிலம்/வசிப்பிடம்", "உங்கள் நிரந்தர வசிப்பிடம் அல்லது டொமிசைல் மாநிலம் எது?"),
        },
    }
    localized = questions.get(normalized_language, questions["en"])

    return [
        VoiceEligibilityCriterion(
            key="income",
            label=localized["income"][0],
            question=localized["income"][1],
            expected="Annual family income should be within the scheme income limit.",
            description=f"Income requirement for {scheme_name}.",
        ),
        VoiceEligibilityCriterion(
            key="category",
            label=localized["category"][0],
            question=localized["category"][1],
            expected="Applicant should belong to an eligible caste/category, if the scheme has a category rule.",
            description=f"Category requirement for {scheme_name}.",
        ),
        VoiceEligibilityCriterion(
            key="qualification",
            label=localized["qualification"][0],
            question=localized["qualification"][1],
            expected="Applicant should be a student with the required academic qualification or course enrollment.",
            description=f"Academic requirement for {scheme_name}.",
        ),
        VoiceEligibilityCriterion(
            key="age",
            label=localized["age"][0],
            question=localized["age"][1],
            expected="Applicant age should be within the eligible age range, if specified.",
            description=f"Age requirement for {scheme_name}.",
        ),
        VoiceEligibilityCriterion(
            key="state",
            label=localized["state"][0],
            question=localized["state"][1],
            expected="Applicant should satisfy the scheme state or domicile requirement.",
            description=f"State or domicile requirement for {scheme_name}.",
        ),
    ]


def clean_groq_json(raw: str) -> str:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("[")
    end = cleaned.rfind("]")
    if start != -1 and end != -1 and end > start:
        return cleaned[start : end + 1]
    return cleaned


def get_voice_eligibility_criteria_with_groq(
    scheme_name: str,
    language: str,
) -> list[VoiceEligibilityCriterion]:
    normalized_language = normalize_language_code(language)
    fallback = default_voice_eligibility_criteria(scheme_name, normalized_language)
    if not GROQ_API_KEY:
        return fallback

    language_name = {
        "en": "English",
        "hi": "Hindi",
        "te": "Telugu",
        "ta": "Tamil",
    }.get(normalized_language, "English")

    try:
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You return structured scholarship eligibility criteria as JSON only. "
                        "Do not include markdown or explanatory text. "
                        "Each item must include key, label, question, expected, and description. "
                        "Use stable lowercase keys such as income, category, qualification, age, state."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Scheme: {scheme_name}\n"
                        f"Question language: {language_name}\n"
                        "Return 4 to 6 eligibility criteria for this Indian government scholarship. "
                        "Use this exact JSON array shape: "
                        '[{"key":"income","label":"Annual income","question":"What is your annual family income?",'
                        '"expected":"Income should be below the applicable limit.",'
                        '"description":"Income condition"}]'
                    ),
                },
            ],
            temperature=0.1,
        )
        message = completion.choices[0].message.content if completion.choices else None
        if not message:
            return fallback
        parsed = json.loads(clean_groq_json(message))
        criteria: list[VoiceEligibilityCriterion] = []
        if isinstance(parsed, list):
            for item in parsed[:6]:
                if not isinstance(item, dict):
                    continue
                key = str(item.get("key", "")).strip().lower()
                question = str(item.get("question", "")).strip()
                if not key or not question:
                    continue
                criteria.append(
                    VoiceEligibilityCriterion(
                        key=key,
                        label=str(item.get("label") or key.replace("_", " ").title()),
                        question=question,
                        expected=str(item.get("expected", "")).strip()
                        or "Applicant should satisfy this criterion.",
                        description=str(item.get("description", "")).strip(),
                    )
                )
        return criteria or fallback
    except Exception:
        return fallback
