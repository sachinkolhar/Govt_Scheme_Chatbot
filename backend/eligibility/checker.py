"""Eligibility matching helpers."""
import re
from typing import Optional

import pandas as pd

try:
    from ..models.database import User
    from ..models.schemas import EligibilityRequest, SchemeResult
    from ..search.semantic import get_dataframe, row_to_result, semantic_candidates
except ImportError:
    from models.database import User
    from models.schemas import EligibilityRequest, SchemeResult
    from search.semantic import get_dataframe, row_to_result, semantic_candidates


def profile_to_query(profile: EligibilityRequest) -> str:
    parts = []
    if profile.age is not None:
        parts.append(f"age {profile.age}")
    if profile.gender:
        parts.append(profile.gender)
    if profile.state:
        parts.append(profile.state)
    if profile.occupation:
        parts.append(profile.occupation)
    if profile.category:
        parts.append(profile.category)
    if profile.income is not None:
        parts.append(f"income {int(profile.income)}")
    if profile.student_status:
        parts.append("student")
    if profile.farmer_status:
        parts.append("farmer")
    if profile.disability:
        parts.append("disability")
    return " ".join(parts) if parts else "government welfare scheme"


def text_blob(row: pd.Series) -> str:
    return " ".join(
        [
            str(row.get("scheme_name", "")),
            str(row.get("details", "")),
            str(row.get("eligibility", "")),
            str(row.get("benefits", "")),
            str(row.get("schemeCategory", "")),
            str(row.get("tags", "")),
            str(row.get("level", "")),
        ]
    ).lower()


def parse_income_limit(text: str) -> Optional[float]:
    lowered = text.lower()
    patterns = [
        r"(?:income|annual income|family income)\s*(?:below|under|less than|upto|up to|not exceed(?:ing)?)\s*rs\.?\s*([\d,]+)",
        r"(?:income|annual income|family income)\s*(?:below|under|less than|upto|up to|not exceed(?:ing)?)\s*([\d,]+)",
    ]
    for pat in patterns:
        match = re.search(pat, lowered)
        if match:
            return float(match.group(1).replace(",", ""))
    return None


def age_is_eligible(user_age: Optional[int], text: str) -> bool:
    if user_age is None:
        return True
    lowered = text.lower()

    range_match = re.search(r"(\d{1,2})\s*(?:to|\-|\u2013)\s*(\d{1,2})\s*year", lowered)
    if range_match:
        min_age = int(range_match.group(1))
        max_age = int(range_match.group(2))
        return min_age <= user_age <= max_age

    min_match = re.search(r"(?:above|greater than|minimum)\s*(\d{1,2})\s*year", lowered)
    if min_match and user_age < int(min_match.group(1)):
        return False

    max_match = re.search(r"(?:below|less than|maximum|up to|upto)\s*(\d{1,2})\s*year", lowered)
    if max_match and user_age > int(max_match.group(1)):
        return False

    return True


def gender_is_eligible(user_gender: Optional[str], text: str) -> bool:
    if not user_gender:
        return True

    g = user_gender.lower().strip()
    lowered = text.lower()
    female_only = any(k in lowered for k in ["women", "woman", "female", "girl"])
    male_only = any(k in lowered for k in ["male", "men", "boy"])

    if female_only and g not in ["female", "woman", "women", "f"]:
        return False
    if male_only and g not in ["male", "man", "men", "m"]:
        return False
    return True


def category_is_eligible(user_category: Optional[str], text: str) -> bool:
    if not user_category:
        return True

    lowered = text.lower()
    category = user_category.lower().strip()
    category_tokens = {
        "sc": ["sc", "scheduled caste"],
        "st": ["st", "scheduled tribe"],
        "obc": ["obc", "other backward"],
        "general": ["general", "unreserved"],
    }

    if category not in category_tokens:
        return True

    mentioned = any(token in lowered for values in category_tokens.values() for token in values)
    if not mentioned:
        return True

    return any(token in lowered for token in category_tokens[category])


def state_is_eligible(user_state: Optional[str], text: str) -> bool:
    if not user_state:
        return True

    lowered = text.lower()
    normalized_state = user_state.lower().strip()

    if any(k in lowered for k in ["all india", "pan india", "central sector", "nationwide"]):
        return True

    common_state_markers = [
        "andhra", "arunachal", "assam", "bihar", "chhattisgarh", "goa", "gujarat",
        "haryana", "himachal", "jharkhand", "karnataka", "kerala", "madhya pradesh",
        "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha",
        "punjab", "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura",
        "uttar pradesh", "uttarakhand", "west bengal", "delhi", "jammu", "ladakh",
    ]
    mentions_state = any(s in lowered for s in common_state_markers)
    if not mentions_state:
        return True

    return normalized_state in lowered


def is_state_compatible_before_scoring(user_state: Optional[str], row: pd.Series) -> bool:
    """
    Strict state filtering BEFORE scoring.
    Only allows schemes that:
    1. Match the user's state, OR
    2. Are explicitly national schemes
    
    This prevents multi-state schemes from other regions being shown.
    """
    if not user_state:
        # No state filter - allow all schemes
        return True
    
    # Extract scheme info
    level = str(row.get("level", "")).lower().strip()
    eligibility = str(row.get("eligibility", "")).lower()
    details = str(row.get("details", "")).lower()
    scheme_blob = text_blob(row)
    
    # Check for national schemes
    national_keywords = ["all india", "pan india", "national", "india", "central sector", "nationwide", "all states"]
    if any(k in scheme_blob for k in national_keywords):
        return True
    
    # Check level field for state markers
    if any(k in level for k in national_keywords):
        return True
    
    # Normalize user state
    normalized_state = user_state.lower().strip()
    
    # Check if scheme is specific to user's state
    if normalized_state in scheme_blob:
        return True
    
    # Check for partial state name matches (e.g., "Karnataka" in "Karnataka Government")
    state_variants = {
        "andhra pradesh": ["andhra", "ap"],
        "arunachal pradesh": ["arunachal"],
        "tamil nadu": ["tamil nadu", "tn"],
        "uttar pradesh": ["uttar pradesh", "up"],
        "madhya pradesh": ["madhya pradesh", "mp"],
        "himachal pradesh": ["himachal"],
    }
    
    user_state_lower = normalized_state.lower()
    for full_state, variants in state_variants.items():
        if user_state_lower == full_state or any(v == user_state_lower for v in variants):
            if any(v in scheme_blob for v in variants) or full_state in scheme_blob:
                return True
    
    # If scheme mentions ANY state but NOT the user's state, exclude it
    common_state_markers = [
        "andhra", "arunachal", "assam", "bihar", "chhattisgarh", "goa", "gujarat",
        "haryana", "himachal", "jharkhand", "karnataka", "kerala", "madhya", "pradesh",
        "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha",
        "punjab", "rajasthan", "sikkim", "tamil", "telangana", "tripura",
        "uttarakhand", "west bengal", "delhi", "jammu", "ladakh",
    ]
    
    mentions_any_state = any(s in scheme_blob for s in common_state_markers)
    if mentions_any_state:
        # Scheme mentions a state, but not the user's state - exclude it
        return False
    
    # Scheme doesn't mention any specific state - allow it (likely national/general)
    return True


def occupation_is_eligible(profile: EligibilityRequest, text: str) -> bool:
    lowered = text.lower()

    if profile.student_status and any(k in lowered for k in ["student", "scholarship"]):
        return True
    if profile.farmer_status and any(k in lowered for k in ["farmer", "agriculture", "kisan"]):
        return True

    if profile.occupation:
        occ = profile.occupation.lower().strip()
        occupation_keywords = {
            "student": ["student", "scholarship"],
            "farmer": ["farmer", "agriculture", "kisan"],
            "worker": ["worker", "labor", "labour"],
        }
        if occ in occupation_keywords:
            return any(k in lowered for k in occupation_keywords[occ]) or "for all" in lowered
    return True


def income_is_eligible(user_income: Optional[float], text: str) -> bool:
    if user_income is None:
        return True
    limit = parse_income_limit(text)
    if limit is None:
        return True
    return user_income <= limit


def disability_is_eligible(is_disabled: bool, text: str) -> bool:
    lowered = text.lower()
    disability_targeted = any(k in lowered for k in ["disability", "disabled", "divyang", "pwd"])
    if disability_targeted and not is_disabled:
        return False
    return True


def is_eligible(profile: EligibilityRequest, row: pd.Series) -> bool:
    blob = text_blob(row)
    return (
        age_is_eligible(profile.age, blob)
        and gender_is_eligible(profile.gender, blob)
        and category_is_eligible(profile.category, blob)
        and state_is_eligible(profile.state, blob)
        and occupation_is_eligible(profile, blob)
        and income_is_eligible(profile.income, blob)
        and disability_is_eligible(profile.disability, blob)
    )


def calculate_match_score(profile: EligibilityRequest, row: pd.Series) -> tuple[int, list[str]]:
    """
    Calculate match score (0-100) and reasons for recommendation.
    
    Scoring weights:
    - State Match: 30 points
    - Category Match: 20 points
    - Occupation Match: 15 points
    - Student Status Match: 15 points
    - Income Eligibility: 10 points
    - Age Eligibility: 10 points
    
    Returns: (score, reasons_list)
    """
    score = 0
    reasons = []
    blob = text_blob(row)
    
    # State match (30 points)
    if profile.state and state_is_eligible(profile.state, blob):
        state_normalized = profile.state.lower().strip()
        if state_normalized in blob.lower():
            score += 30
            reasons.append(f"{profile.state} resident")
        elif any(k in blob.lower() for k in ["all india", "pan india", "central sector", "nationwide"]):
            score += 15  # Partial credit for pan-india schemes
            reasons.append("Pan-India scheme")
    
    # Category match (20 points)
    if profile.category:
        if category_is_eligible(profile.category, blob):
            score += 20
            reasons.append(f"{profile.category} category")
    
    # Occupation match (15 points)
    if profile.occupation:
        if occupation_is_eligible(profile, blob):
            score += 15
            if profile.student_status:
                reasons.append("Student")
            elif profile.farmer_status:
                reasons.append("Farmer")
            else:
                reasons.append(profile.occupation)
    elif profile.student_status and any(k in blob.lower() for k in ["student", "scholarship"]):
        score += 15
        reasons.append("Student")
    elif profile.farmer_status and any(k in blob.lower() for k in ["farmer", "agriculture", "kisan"]):
        score += 15
        reasons.append("Farmer")
    
    # Student status match (15 points)
    if profile.student_status and any(k in blob.lower() for k in ["student", "scholarship", "education"]):
        if "Student" not in reasons:  # Avoid duplication
            score += 15
            reasons.append("Student status")
    
    # Income eligibility (10 points)
    if profile.income and income_is_eligible(profile.income, blob):
        score += 10
        reasons.append("Income within eligible limit")
    
    # Age eligibility (10 points)
    if profile.age and age_is_eligible(profile.age, blob):
        score += 10
        reasons.append("Age eligible")
    
    # Cap at 100
    score = min(score, 100)
    
    return score, reasons


def get_personalized_schemes(profile: EligibilityRequest, top_k: int, user_id: Optional[int] = None) -> list[SchemeResult]:
    from ..config.database import SessionLocal
    from ..models.database import Favorite
    
    profile_query = profile_to_query(profile)
    candidates = semantic_candidates(profile_query, top_k * 8)
    df = get_dataframe()

    # Get user's favorite scheme IDs if user_id provided
    favorite_scheme_ids = set()
    if user_id:
        try:
            db = SessionLocal()
            favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
            favorite_scheme_ids = {f.scheme_id for f in favorites}
            db.close()
        except Exception:
            pass  # Silently ignore database errors

    chosen: list[tuple[SchemeResult, int]] = []  # (SchemeResult, score_for_sorting)
    seen: set[int] = set()

    # Process semantic candidates with state filtering BEFORE eligibility
    for idx, score in candidates:
        if idx in seen:
            continue
        row = df.iloc[idx]
        
        # Apply state filtering BEFORE eligibility check
        if not is_state_compatible_before_scoring(profile.state, row):
            continue
        
        if is_eligible(profile, row):
            match_score, reasons = calculate_match_score(profile, row)
            scheme_name = str(row.get("scheme_name", ""))
            scheme_id = f"{idx}:{scheme_name}"  # Unique identifier
            is_fav = scheme_id in favorite_scheme_ids
            result = row_to_result(row, score, match_score, reasons, is_fav)
            chosen.append((result, match_score))
            seen.add(idx)
        if len(chosen) >= top_k:
            break

    # Fill remaining slots with non-semantic results if needed
    if len(chosen) < top_k:
        for idx, row in df.iterrows():
            if idx in seen:
                continue
            
            # Apply state filtering BEFORE eligibility check
            if not is_state_compatible_before_scoring(profile.state, row):
                continue
            
            if is_eligible(profile, row):
                match_score, reasons = calculate_match_score(profile, row)
                scheme_name = str(row.get("scheme_name", ""))
                scheme_id = f"{idx}:{scheme_name}"
                is_fav = scheme_id in favorite_scheme_ids
                result = row_to_result(row, 0.0, match_score, reasons, is_fav)
                chosen.append((result, match_score))
                seen.add(int(idx))
            if len(chosen) >= top_k:
                break

    # Sort by match score descending
    chosen.sort(key=lambda x: x[1], reverse=True)
    
    return [result for result, _ in chosen[:top_k]]


def profile_from_user(user: User, top_k: int) -> EligibilityRequest:
    return EligibilityRequest(
        age=user.age,
        gender=user.gender,
        state=user.state,
        occupation=user.occupation,
        income=user.income,
        category=user.category,
        disability=bool(user.disability),
        student_status=bool(user.student_status),
        farmer_status=bool(user.farmer_status),
        top_k=top_k,
    )
