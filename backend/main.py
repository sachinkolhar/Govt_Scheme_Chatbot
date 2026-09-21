import os
from importlib import import_module
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    import faiss
except ImportError:
    faiss = None

try:
    import torch
except ImportError:
    torch = None

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

try:
    import whisper
except ImportError:
    whisper = None


_PREFIX = f"{__package__}." if __package__ else ""


def _module(path: str):
    return import_module(f"{_PREFIX}{path}")


settings = _module("config.settings")
schemas = _module("models.schemas")
semantic = _module("search.semantic")
NO_DATA_PROMPT = settings.NO_DATA_PROMPT

ChatRequest = schemas.ChatRequest
ChatState = schemas.ChatState
SchemeResult = schemas.SchemeResult
SpeechRequest = schemas.SpeechRequest
format_speech_error = _module("utils.errors").format_speech_error
normalize_language_code = _module("utils.errors").normalize_language_code

chat = _module("chat.routes").chat
chat_stream = _module("chat.routes").chat_stream
chat_state_store = _module("chat.state").chat_state_store
generate_answer_with_groq = _module("chat.groq_client").generate_answer_with_groq

semantic_candidates = semantic.semantic_candidates
row_to_result = semantic.row_to_result
get_db_relevant_schemes = semantic.get_db_relevant_schemes
web_search_relevant_schemes = _module("search.web").web_search_relevant_schemes
summarize_web_schemes_with_groq = _module("search.web").summarize_web_schemes_with_groq

transcribe_audio = _module("voice.whisper").transcribe_audio
synthesize_audio = _module("voice.gtts").synthesize_audio
voice_assistant_chat = _module("voice.routes").voice_assistant_chat
voice_eligibility_criteria = _module("voice.routes").voice_eligibility_criteria


if torch is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    torch.cuda.is_available = lambda: False  # type: ignore
    _orig_torch_load = torch.load  # type: ignore

    def _cpu_torch_load(*args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("map_location", "cpu")
        kwargs.setdefault("weights_only", False)
        return _orig_torch_load(*args, **kwargs)

    torch.load = _cpu_torch_load  # type: ignore


_module("config.database").init_database()

print("Loading semantic encoder ...")
try:
    encoder = joblib.load(os.path.join(settings.MODEL_DIR, "semantic_encoder.pkl"))
except Exception as exc:
    print(f"Warning: semantic encoder unavailable: {exc}")
    encoder = None

print("Loading FAISS index ...")
if faiss is not None:
    try:
        faiss_index = faiss.read_index(os.path.join(settings.MODEL_DIR, "scheme_index.faiss"))
    except Exception as exc:
        print(f"Warning: FAISS index unavailable: {exc}")
        faiss_index = None
else:
    print("Warning: faiss not installed; semantic search disabled.")
    faiss_index = None

print("Loading dataset ...")
df = pd.read_csv(os.path.join(settings.DATA_DIR, "govt_schemes.csv")).fillna("")
semantic.configure_search_resources(encoder, faiss_index, df)
print(f"Ready - {len(df)} schemes loaded.")

print("Loading Whisper model (this may take 2-3 minutes on first run)...")
whisper_model = None
if whisper is not None:
    try:
        whisper_model = whisper.load_model("small", device="cpu")
        print("✓ Whisper model loaded successfully")
    except Exception as exc:
        print(f"Warning: Whisper model unavailable: {exc}")
else:
    print("Warning: whisper not installed; speech recognition disabled.")

app = FastAPI(title="Govt Scheme Assistant API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router_path in (
    "auth.routes",
    "chat.routes",
    "search.routes",
    "eligibility.routes",
    "voice.routes",
    "ivr.routes",
    "reminders.routes",
    "documents.routes",
    "profile_assets.routes",
):
    app.include_router(_module(router_path).router)


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "total_schemes": len(df),
        "database": "connected",
        "whisper_model": "ready" if whisper_model is not None else "unavailable",
        "encoder": "ready" if encoder is not None else "unavailable",
    }
