"""Chat API routes."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

try:
    from ..models.schemas import ChatRequest, ChatResponse
    from .processor import process_chat, stream_chat_events
except ImportError:
    from models.schemas import ChatRequest, ChatResponse
    from chat.processor import process_chat, stream_chat_events


router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return process_chat(payload)


@router.post("/chat/stream")
async def chat_stream(payload: ChatRequest) -> StreamingResponse:
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return StreamingResponse(stream_chat_events(payload), media_type="text/event-stream")
