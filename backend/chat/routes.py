"""Chat API routes."""
import logging
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

try:
    from ..models.schemas import ChatRequest, ChatResponse
    from .processor import process_chat, stream_chat_events
except ImportError:
    from models.schemas import ChatRequest, ChatResponse
    from chat.processor import process_chat, stream_chat_events


router = APIRouter(prefix="/api", tags=["chat"])
logger = logging.getLogger(__name__)


def _safe_stream(payload: ChatRequest, request_id: str):
    """Ensure an internal failure becomes a client-safe SSE error and completion."""
    completed = False
    try:
        for event in stream_chat_events(payload):
            if '"type": "done"' in event:
                completed = True
            yield event
    except Exception as error:
        logger.warning("chat stream failed", extra={"request_id": request_id, "error_category": type(error).__name__})
        yield 'data: {"type":"error","text":"The chat service could not complete this request. Please try again."}\n\n'
    if not completed:
        yield 'data: {"type":"done"}\n\n'


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    request_id = uuid4().hex
    logger.info("chat request accepted", extra={"request_id": request_id, "conversation_id": payload.conversation_id or "anonymous"})
    return process_chat(payload)


@router.post("/chat/stream")
async def chat_stream(payload: ChatRequest) -> StreamingResponse:
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    request_id = uuid4().hex
    logger.info("chat stream accepted", extra={"request_id": request_id, "conversation_id": payload.conversation_id or "anonymous"})
    return StreamingResponse(_safe_stream(payload, request_id), media_type="text/event-stream")
