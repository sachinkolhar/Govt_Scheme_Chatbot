"""In-memory chat state management."""
import time

try:
    from ..config.settings import CHAT_STATE_TTL_SECONDS
    from ..models.schemas import ChatRequest, ChatState
except ImportError:
    from config.settings import CHAT_STATE_TTL_SECONDS
    from models.schemas import ChatRequest, ChatState


chat_state_store: dict[str, ChatState] = {}


def conversation_key(payload: ChatRequest) -> str:
    raw = (payload.conversation_id or "").strip()
    if raw:
        return raw[:120]
    return "anonymous"


def cleanup_chat_state() -> None:
    now = time.time()
    expired = [
        key
        for key, value in chat_state_store.items()
        if (now - value.updated_at) > CHAT_STATE_TTL_SECONDS
    ]
    for key in expired:
        del chat_state_store[key]


def get_chat_state(key: str) -> ChatState:
    cleanup_chat_state()
    state = chat_state_store.get(key)
    if not state:
        state = ChatState()
        chat_state_store[key] = state
    return state


def save_chat_state(key: str, state: ChatState) -> None:
    state.updated_at = time.time()
    chat_state_store[key] = state
