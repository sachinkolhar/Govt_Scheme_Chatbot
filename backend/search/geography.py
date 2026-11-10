"""Conservative geographic applicability checks for scheme candidates."""
import re
from typing import Optional


_PLACES = (
    "Andhra Pradesh", "Arunachal Pradesh", "Chhattisgarh", "Himachal Pradesh",
    "Madhya Pradesh", "Tamil Nadu", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Jammu and Kashmir", "Dadra & Nagar Haveli and Daman & Diu",
    "Dadra and Nagar Haveli and Daman and Diu", "Andaman and Nicobar Islands",
    "Andaman & Nicobar Islands", "Puducherry", "Lakshadweep", "Chandigarh",
    "Delhi", "Ladakh", "Karnataka", "Kerala", "Maharashtra", "Telangana",
    "Rajasthan", "Gujarat", "Punjab", "Haryana", "Bihar", "Jharkhand",
    "Odisha", "Assam", "Goa", "Sikkim", "Tripura", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland",
)
_NATIONAL_MARKERS = (
    "all india", "pan india", "nationwide", "across india", "throughout india",
    "across the country", "all states", "central government scheme",
    "central sector scheme", "centrally sponsored scheme",
)


def _row_get(row, field: str, default=""):
    if hasattr(row, "get"):
        return row.get(field, default)
    return getattr(row, field, default)


def geographic_classification(row) -> str:
    """Classify explicit national/state scope, preserving UNKNOWN separately."""
    level = str(_row_get(row, "level", "") or "").strip().casefold()
    fields = ("scheme_name", "details", "eligibility", "benefits", "application", "documents", "tags", "schemeCategory", "level")
    blob = " ".join(str(_row_get(row, field, "") or "") for field in fields)
    normalized_blob = re.sub(r"[^a-z0-9]+", " ", blob.casefold()).strip()
    if level == "central" or any(marker in normalized_blob for marker in _NATIONAL_MARKERS):
        return "CENTRAL"
    normalized_places = {
        re.sub(r"[^a-z0-9]+", " ", place.casefold()).strip(): place
        for place in _PLACES
    }
    present = [place for normalized, place in normalized_places.items()
               if re.search(r"\b" + re.escape(normalized) + r"\b", normalized_blob)]
    if present:
        # Most records describe one jurisdiction. If text mentions several, do
        # not choose one arbitrarily; retain the ambiguity as unknown.
        canonical = {re.sub(r"[^a-z0-9]+", " ", place.casefold()).strip() for place in present}
        if len(canonical) == 1:
            return present[0]
    return "UNKNOWN"


def geographic_applicability(row, user_state: Optional[str]) -> str:
    """Return applicable, incompatible, or unknown from actual row text/level."""
    if not user_state:
        return "applicable"
    normalized_state = re.sub(r"[^a-z0-9]+", " ", user_state.casefold()).strip()
    classification = geographic_classification(row)
    if classification == "CENTRAL":
        return "applicable"
    if classification == "UNKNOWN":
        return "unknown"
    normalized_classification = re.sub(r"[^a-z0-9]+", " ", classification.casefold()).strip()
    return "applicable" if normalized_state == normalized_classification else "incompatible"


def is_geographically_applicable(row, user_state: Optional[str]) -> bool:
    """Keep only confirmed compatible rows; unknown geography fails closed."""
    return geographic_applicability(row, user_state) == "applicable"
