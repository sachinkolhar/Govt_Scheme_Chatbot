"""Search API routes."""
from fastapi import APIRouter

try:
    from ..models.schemas import CategoryResponse, SearchRequest, SearchResponse
    from .semantic import get_dataframe, row_to_result, semantic_candidates
except ImportError:
    from models.schemas import CategoryResponse, SearchRequest, SearchResponse
    from search.semantic import get_dataframe, row_to_result, semantic_candidates


router = APIRouter(prefix="/api", tags=["search"])


@router.post("/search", response_model=SearchResponse)
def search_schemes(payload: SearchRequest) -> SearchResponse:
    candidates = semantic_candidates(payload.query, payload.top_k)
    df = get_dataframe()
    results = [row_to_result(df.iloc[idx], score) for idx, score in candidates]
    return SearchResponse(query=payload.query, results=results)


@router.get("/categories", response_model=list[CategoryResponse])
def categories() -> list[CategoryResponse]:
    df = get_dataframe()
    categories_series = df.get("schemeCategory")
    if categories_series is None:
        return []
    cleaned = categories_series.astype(str)
    cleaned = cleaned[cleaned.str.strip() != ""]
    counts = cleaned.value_counts().head(15)
    return [CategoryResponse(category=str(cat), count=int(cnt)) for cat, cnt in counts.items()]
