"""Lightweight, deterministic intent and section detection for scheme chat."""
from dataclasses import asdict, dataclass
import re
from typing import Optional, Sequence


@dataclass(frozen=True)
class IntentResult:
    intent: str
    confidence: float
    scheme_name: Optional[str] = None
    requested_section: Optional[str] = None
    target_group: Optional[str] = None

    def to_dict(self) -> dict:
        value = asdict(self)
        if value.get("target_group") is None:
            value.pop("target_group")
        return value


_SECTION_PATTERNS = {
    "eligibility": ("eligibility", "eligible", "who can apply", "am i eligible", "qualify"),
    "application": ("how to apply", "apply", "application process", "steps to apply"),
    "benefits": ("benefits", "advantage", "what do i get"),
    "documents": ("documents", "document required", "papers required"),
    "details": ("details", "about this scheme", "overview", "what is this"),
}


_TARGET_GROUP_PATTERNS = (
    ("senior_citizen", (r"\bsenior\s+citizens?\b", r"\bold[- ]age\b", r"\belderly\b", r"\bold\s+persons?\b", r"\bvridh", r"\bvriddh", r"\bbriddh", r"\bbaristha\s+nagarika\b")),
    ("construction_worker", (r"\bconstruction\s+workers?\b", r"\bbuilding\s+workers?\b", r"\bbocw\b", r"\bbuilding\s+and\s+other\s+construction\b")),
    ("law_graduate", (r"\blaw\s+graduates?\b", r"\blawyers?\b")),
    ("farmer", (r"\bfarmers?\b", r"\bkisans?\b", r"\bkrishak\b")),
    ("student", (r"\bstudents?\b", r"\bscholarship\b")),
    ("women", (r"\bwomen\b", r"\bwoman\b", r"\bwomen's\b", r"\bwidow\b")),
    ("disability", (r"\bpersons? with disabilit", r"\bdisabled\b", r"\bdivyang\b", r"\bpwd\b")),
    ("worker", (r"\bworkers?\b", r"\blabou?rer?s?\b", r"\bunorganised workers?\b")),
)


def detect_target_group(text: str) -> Optional[str]:
    """Extract the requested beneficiary group from the existing query intent."""
    lowered = (text or "").lower()
    for target_group, patterns in _TARGET_GROUP_PATTERNS:
        if any(re.search(pattern, lowered) for pattern in patterns):
            return target_group
    return None


def detect_intent(text: str, scheme_names: Optional[Sequence[str]] = None) -> IntentResult:
    """Detect common scheme intents without asking a model to guess scheme names."""
    query = re.sub(r"\s+", " ", (text or "").strip().lower())
    target_group = detect_target_group(query)
    section = next(
        (name for name, patterns in _SECTION_PATTERNS.items()
         if any(pattern in query for pattern in patterns)),
        None,
    )
    scheme = None
    for name in sorted((scheme_names or ()), key=len, reverse=True):
        if name and name.lower() in query:
            scheme = name
            break

    if not query:
        return IntentResult("unknown", 0.0, requested_section=section, target_group=target_group)
    if scheme and any(phrase in query for phrase in ("can i get", "can i apply", "am i eligible", "do i qualify")):
        return IntentResult("check_eligibility", 0.95, scheme, section or "eligibility", target_group)
    if any(phrase in query for phrase in ("can i get", "am i eligible", "do i qualify")) and not any(
        plural in query for plural in ("schemes", "scheme available", "schemes available", "schemes can i get")
    ):
        return IntentResult("check_eligibility", 0.9, None, section or "eligibility", target_group)
    if re.fullmatch(r"(yes|no|yeah|yep|nope|haan|han|nahi|na|ஆம்|కాదు|అవును)[.!? ]*", query):
        intent, confidence = "follow_up", 0.95
    elif any(x in query for x in ("compare", "difference between", "vs.", " versus ")):
        intent, confidence = "compare_schemes", 0.9
    elif any(x in query for x in ("application status", "track my application", "status of my application")):
        intent, confidence = "application_status", 0.9
    elif section == "eligibility":
        intent, confidence = "check_eligibility", 0.9
    elif section == "benefits":
        intent, confidence = "benefits", 0.9
    elif section == "documents":
        intent, confidence = "documents", 0.9
    elif section == "application":
        intent, confidence = "how_to_apply", 0.9
    elif section == "details" and scheme:
        intent, confidence = "scheme_details", 0.85
    elif any(x in query for x in ("another scheme", "other schemes", "tell me more", "more about it", "which one", "what about this", "what about that", "tell me about the second", "tell me about the first", "tell me about the third")):
        intent, confidence = "follow_up", 0.8
    elif re.search(r"\b(first|second|third|1st|2nd|3rd)\b", query):
        intent, confidence = "follow_up", 0.85
    elif any(x in query for x in ("hello", "hi", "hey", "good morning", "good evening")):
        intent, confidence = "greeting", 0.95
    elif any(x in query for x in ("search the web", "search online", "official website", "look online")):
        intent, confidence = "web_search_request", 0.9
    elif any(x in query for x in ("scheme", "schemes", "yojana", "scholarship", "pension", "what can i get", "available for me")):
        intent, confidence = "find_scheme", 0.75
    else:
        intent, confidence = "unknown", 0.0

    if scheme and intent in {"find_scheme", "unknown"}:
        intent, confidence = "scheme_details", 0.85
    return IntentResult(intent, confidence, scheme, section, target_group)
