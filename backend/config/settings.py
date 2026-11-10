"""
Configuration settings and environment variables.
"""
import os
import warnings
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ---- Paths ----
MODEL_DIR = os.path.join(ROOT_DIR, "model")
DATA_DIR = os.path.join(ROOT_DIR, "dataset")

# ---- Security ----
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# ---- Groq API ----
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# ---- FAISS Search ----
# IndexFlatL2 returns squared L2 distances: lower values are closer.
# FAISS_MAX_DISTANCE is the production cutoff. It is disabled unless calibrated.
# FAISS_MIN_SCORE is retained only as an explicitly opted-in legacy compatibility input.
def resolve_faiss_max_distance(environment=None):
    """Resolve the optional squared-L2 cutoff without reinterpreting legacy values."""
    if environment is None:
        environment = os.environ

    configured_distance = environment.get("FAISS_MAX_DISTANCE")
    if configured_distance not in (None, ""):
        return float(configured_distance)

    legacy_score = environment.get("FAISS_MIN_SCORE")
    if legacy_score in (None, ""):
        return None

    warnings.warn(
        "FAISS_MIN_SCORE is deprecated and is ignored unless "
        "FAISS_ENABLE_LEGACY_MIN_SCORE=1; its value is not calibrated as "
        "a squared L2 distance.",
        DeprecationWarning,
        stacklevel=2,
    )
    legacy_opt_in = environment.get("FAISS_ENABLE_LEGACY_MIN_SCORE", "").strip().lower()
    if legacy_opt_in not in {"1", "true", "yes"}:
        return None
    return float(legacy_score)


FAISS_MAX_DISTANCE = resolve_faiss_max_distance()
SEMANTIC_RETRIEVAL_TOP_K = max(1, int(os.getenv("SEMANTIC_RETRIEVAL_TOP_K", "20")))
CHAT_TOP_N = max(1, int(os.getenv("CHAT_TOP_N", "20")))
CHAT_FINAL_K = max(1, int(os.getenv("CHAT_FINAL_K", "5")))
BM25_ENABLED = os.getenv("BM25_ENABLED", "true").strip().lower() in {"1", "true", "yes"}
RERANKER_ENABLED = os.getenv("RERANKER_ENABLED", "true").strip().lower() in {"1", "true", "yes"}
WEB_SEARCH_ENABLED = os.getenv("WEB_SEARCH_ENABLED", "true").strip().lower() in {"1", "true", "yes"}
WEB_SEARCH_MAX_RESULTS = max(1, min(10, int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5"))))
WEB_PAGE_FETCH_TIMEOUT_SECONDS = max(1, min(5, int(os.getenv("WEB_PAGE_FETCH_TIMEOUT_SECONDS", "3"))))
WEB_SEARCH_ALLOWED_DOMAINS = tuple(
    domain.strip().lower().lstrip(".")
    for domain in os.getenv(
        "WEB_SEARCH_ALLOWED_DOMAINS",
        "india.gov.in,mygov.in,myscheme.gov.in,pmkisan.gov.in,scholarships.gov.in,nic.in,gov.in",
    ).split(",") if domain.strip()
)

CONFIDENCE_HIGH_THRESHOLD = float(os.getenv("CONFIDENCE_HIGH_THRESHOLD", "0.75"))
CONFIDENCE_MEDIUM_THRESHOLD = float(os.getenv("CONFIDENCE_MEDIUM_THRESHOLD", "0.45"))
RANK_WEIGHT_SEMANTIC = float(os.getenv("RANK_WEIGHT_SEMANTIC", "0.7"))
RANK_WEIGHT_ELIGIBILITY = float(os.getenv("RANK_WEIGHT_ELIGIBILITY", "0.2"))
RANK_WEIGHT_INTENT = float(os.getenv("RANK_WEIGHT_INTENT", "0.1"))
# Category score adds target-group evidence to ranking; exact category tier is
# sorted before combined score so target mismatch cannot win on vector similarity.
RANK_WEIGHT_CATEGORY = float(os.getenv("RANK_WEIGHT_CATEGORY", "0.25"))

# ---- Chat State ----
CHAT_STATE_TTL_SECONDS = int(os.getenv("CONVERSATION_TTL_SECONDS", os.getenv("CHAT_STATE_TTL_SECONDS", "3600")))
NO_DATA_PROMPT = "sorry i dont have the data, can i give any relevent schemes for you"

# ---- Database ----
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
