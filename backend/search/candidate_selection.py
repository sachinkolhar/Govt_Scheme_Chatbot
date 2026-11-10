"""Final answer candidate validation and stable scheme deduplication."""
from html import unescape
import re
import unicodedata
from typing import Iterable, Optional

try:
    from .geography import geographic_classification
except ImportError:
    from geography import geographic_classification


def _get(record, field: str, default=""):
    if hasattr(record, "get"):
        return record.get(field, default)
    return getattr(record, field, default)


def _normalize_name(value: str) -> str:
    value = unescape(unicodedata.normalize("NFKC", str(value or "")))
    # Remove a trailing acronym alias (e.g. (IGNOAPS)), but retain meaningful
    # parentheticals such as board/authority identifiers.
    def remove_acronym(match):
        alias = match.group(1)
        compact = re.sub(r"[^A-Za-z0-9]", "", alias)
        return "" if len(compact) >= 5 and alias.upper() == alias else match.group(0)
    value = re.sub(r"\s*\(([^()]*)\)\s*$", remove_acronym, value)
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def scheme_identity(record) -> tuple[str, ...]:
    """Prefer stable IDs/slugs; otherwise key by normalized name and scope."""
    for field in ("scheme_id", "canonical_scheme_id", "id", "slug"):
        value = str(_get(record, field, "") or "").strip()
        if value and value.casefold() not in {"nan", "none", "null"}:
            return (field, re.sub(r"\s+", "", value.casefold()))
    name = _normalize_name(_get(record, "scheme_name", ""))
    authority = next((
        _normalize_name(_get(record, field, ""))
        for field in ("authority", "implementing_agency", "department")
        if _get(record, field, "")
    ), "")
    return ("name", name, geographic_classification(record).casefold(), authority)


def deduplicate_schemes(records: Iterable, identity_getter=None) -> list:
    identity_getter = identity_getter or scheme_identity
    unique = []
    seen = set()
    for record in records:
        key = identity_getter(record)
        if key in seen:
            continue
        seen.add(key)
        unique.append(record)
    return unique


def select_final_candidates(candidates, target_group: Optional[str], limit: int) -> list:
    """Drop target-group UNKNOWN/NO_MATCH candidates before answer exposure."""
    if target_group:
        candidates = [
            candidate for candidate in candidates
            if candidate.category_relevance in {"MATCH", "PARTIAL_MATCH"}
        ]
    return deduplicate_schemes(candidates, lambda candidate: scheme_identity(candidate.scheme))[:max(0, limit)]
