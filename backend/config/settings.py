"""
Configuration settings and environment variables.
"""
import os
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
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# ---- FAISS Search ----
# Minimum FAISS similarity score to treat a candidate as a confident DB match.
# For IndexFlatIP (cosine similarity 0–1): values below this fall back to general LLM knowledge.
# Set to -1.0 to disable and always use the top DB result.
FAISS_MIN_SCORE = float(os.getenv("FAISS_MIN_SCORE", "0.2"))

# ---- Chat State ----
CHAT_STATE_TTL_SECONDS = int(os.getenv("CHAT_STATE_TTL_SECONDS", "1800"))
NO_DATA_PROMPT = "sorry i dont have the data, can i give any relevent schemes for you"

# ---- Database ----
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
