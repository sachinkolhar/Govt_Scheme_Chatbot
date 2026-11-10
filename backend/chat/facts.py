"""Conservative extraction of profile-supported facts from user text."""
import re
from typing import Any, Mapping, Optional


_STATES = {
    "andhra pradesh": "Andhra Pradesh", "arunachal pradesh": "Arunachal Pradesh",
    "assam": "Assam", "bihar": "Bihar", "chhattisgarh": "Chhattisgarh",
    "goa": "Goa", "gujarat": "Gujarat", "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh", "jharkhand": "Jharkhand",
    "karnataka": "Karnataka", "kerala": "Kerala", "madhya pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra", "manipur": "Manipur", "meghalaya": "Meghalaya",
    "mizoram": "Mizoram", "nagaland": "Nagaland", "odisha": "Odisha",
    "punjab": "Punjab", "rajasthan": "Rajasthan", "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu", "telangana": "Telangana", "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh", "uttarakhand": "Uttarakhand", "west bengal": "West Bengal",
    "delhi": "Delhi", "jammu and kashmir": "Jammu and Kashmir", "ladakh": "Ladakh",
    "puducherry": "Puducherry",
}


def _income_amount(text: str) -> Optional[int]:
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    word_match = re.search(r"(?i)\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+(lakh|lakhs|lac|lacs|crore|crores|cr|thousand|thousands)\b", text)
    if word_match:
        unit = word_match.group(2).lower()
        multiplier = 100000 if unit.startswith(("lak", "lac")) else 10000000 if unit.startswith(("cro", "cr")) else 1000
        return words[word_match.group(1).lower()] * multiplier
    match = re.search(r"(?i)(?:rs\.?|₹)?\s*(\d+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs|crore|crores|cr|thousand|thousands)\b", text)
    if match:
        value = float(match.group(1))
        unit = match.group(2).lower()
        multiplier = 100000 if unit.startswith(("lak", "lac")) else 10000000 if unit.startswith(("cro", "cr")) else 1000
        return int(value * multiplier)
    match = re.search(r"(?i)(?:income|earning|earn)\D{0,25}(?:rs\.?|₹)?\s*([\d,]+)", text)
    return int(match.group(1).replace(",", "")) if match else None


def extract_user_facts(text: str, existing_profile: Optional[Mapping[str, Any]] = None) -> dict[str, Any]:
    """Return explicit supported facts plus uncertainty/conflict metadata.

    Existing profile values are inspected for contradictions but never mutated or merged.
    """
    text = text or ""
    lowered = text.lower()
    facts: dict[str, Any] = {}
    uncertain: list[str] = []
    conflicts: list[str] = []

    age_match = re.search(r"(?i)\b(?:i am|i'm|age(?:d)?)\s*(\d{1,3})\b((?:\s+and\s+\d{1,3})?)", text)
    age_values = {int(x) for x in re.findall(r"\d{1,3}", age_match.group(0))} if age_match else set()
    if len(age_values) == 1:
        age = next(iter(age_values))
        if 0 < age < 125:
            facts["age"] = age
    elif len(age_values) > 1:
        conflicts.append("age")

    state_mentions = [(name, canonical) for name, canonical in _STATES.items() if re.search(rf"\b{re.escape(name)}\b", lowered)]
    state_values = {canonical for _, canonical in state_mentions}
    if len(state_values) == 1:
        facts["state"] = next(iter(state_values))
    elif len(state_values) > 1:
        conflicts.append("state")

    income = _income_amount(text)
    if income is not None:
        facts["income"] = income

    gender_mentions = re.findall(r"\b(male|female|man|woman)\b", lowered)
    gender_values = {"male" if value in {"male", "man"} else "female" for value in gender_mentions}
    if len(gender_values) == 1:
        facts["gender"] = next(iter(gender_values))
    elif len(gender_values) > 1:
        conflicts.append("gender")

    category_mentions = {value.upper() for value in re.findall(r"\b(sc|st|obc|ews|general)\b", lowered)}
    if len(category_mentions) == 1:
        facts["category"] = next(iter(category_mentions))
    elif len(category_mentions) > 1:
        conflicts.append("category")

    occupations = [value for value in ("farmer", "student", "worker", "self-employed", "unemployed") if value in lowered]
    if len(occupations) == 1:
        facts["occupation"] = occupations[0]
    elif len(occupations) > 1:
        uncertain.append("multiple occupations mentioned")

    if re.search(r"\b(student|college student|school student)\b", lowered) and re.search(r"\b(not a student|no longer a student)\b", lowered): conflicts.append("student_status")
    elif re.search(r"\b(not a student|no longer a student)\b", lowered): facts["student_status"] = False
    elif re.search(r"\b(student|college student|school student)\b", lowered): facts["student_status"] = True
    if re.search(r"\b(farmer|agricultural worker)\b", lowered) and re.search(r"\b(not a farmer)\b", lowered): conflicts.append("farmer_status")
    elif re.search(r"\b(not a farmer)\b", lowered): facts["farmer_status"] = False
    elif re.search(r"\b(farmer|agricultural worker)\b", lowered): facts["farmer_status"] = True
    if re.search(r"\b(disabled|person with disability|divyang|pwd)\b", lowered): facts["disability"] = True
    elif re.search(r"\b(not disabled|no disability)\b", lowered): facts["disability"] = False

    for field, profile_key in (("age", "age"), ("state", "state"), ("income", "income")):
        if field in facts and existing_profile:
            saved = existing_profile.get(profile_key) if isinstance(existing_profile, Mapping) else getattr(existing_profile, profile_key, None)
            if saved is not None and str(saved).lower() != str(facts[field]).lower():
                conflicts.append(field)
    if re.search(r"\b(maybe|perhaps|not sure|might be)\b", lowered):
        uncertain.append("statement contains uncertainty")
    facts["_uncertain"] = uncertain
    facts["_conflicts"] = sorted(set(conflicts))
    return facts
