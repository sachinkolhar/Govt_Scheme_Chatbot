"""Web search helpers for official government scheme fallback results."""
from urllib.parse import urlparse

try:
    from ..config.settings import GROQ_API_KEY, GROQ_MODEL
    from ..models.schemas import SchemeResult
except ImportError:
    from config.settings import GROQ_API_KEY, GROQ_MODEL
    from models.schemas import SchemeResult


def _is_allowed_web_source(url: str) -> bool:
    try:
        hostname = (urlparse(url).hostname or "").lower()
    except Exception:
        return False
    allowed_suffixes = ("gov.in", "nic.in", "india.gov.in", "mygov.in")
    return any(hostname.endswith(suffix) for suffix in allowed_suffixes)


def web_search_relevant_schemes(query: str, limit: int = 5) -> list[SchemeResult]:
    try:
        from duckduckgo_search import DDGS
    except Exception:
        return []

    max_needed = max(1, min(limit, 5))
    seen_names: set[str] = set()
    results: list[SchemeResult] = []

    try:
        with DDGS() as ddgs:
            raw_results = ddgs.text(
                f"{query} india government scheme official",
                max_results=20,
            )
            for rank, item in enumerate(raw_results, start=1):
                title = str(item.get("title", "")).strip()
                body = str(item.get("body", "")).strip()
                href = str(item.get("href", "")).strip()
                if not title or not href:
                    continue
                if not _is_allowed_web_source(href):
                    continue
                normalized_name = title.lower()
                if normalized_name in seen_names:
                    continue
                seen_names.add(normalized_name)

                results.append(
                    SchemeResult(
                        scheme_name=title,
                        details=body or "Found from official web source.",
                        benefits="Refer official source for confirmed benefits.",
                        eligibility="Refer official source for confirmed eligibility.",
                        application=href,
                        documents="Check official portal for required documents.",
                        level="",
                        schemeCategory="Web",
                        tags="web,official",
                        score=float(max(0.0, 1.0 - (rank - 1) * 0.05)),
                    )
                )
                if len(results) >= max_needed:
                    break
    except Exception:
        return []

    return results


def summarize_web_schemes_with_groq(query: str, schemes: list[SchemeResult]) -> str:
    if not schemes:
        return "Sorry, I could not find relevant schemes right now."

    fallback = f"I found {len(schemes)} relevant schemes from official web sources."
    if not GROQ_API_KEY:
        return fallback

    snippet_lines = []
    for item in schemes[:5]:
        snippet_lines.append(
            f"- {item.scheme_name}: {item.details[:180]} (Source: {item.application})"
        )
    snippets = "\n".join(snippet_lines)

    try:
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You summarize government scheme web search findings. "
                        "Be concise and do not add information outside provided snippets."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Question: {query}\n\n"
                        f"Web snippets:\n{snippets}\n\n"
                        "Write a short response in 2-3 lines before listing schemes."
                    ),
                },
            ],
            temperature=0.2,
        )
        message = completion.choices[0].message.content if completion.choices else None
        if message and message.strip():
            return message.strip()
    except Exception:
        return fallback

    return fallback
