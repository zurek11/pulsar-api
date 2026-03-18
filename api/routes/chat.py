"""Chat endpoints — POST /api/chat (SSE stream) and DELETE /api/chat/history."""

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from api.deps import get_rag_engine
from llm.streaming import tokens_to_sse
from models.schemas import ChatRequest, StatusResponse
from rag.engine import RAGEngine

router = APIRouter(prefix="/api")


@router.post("/chat")
async def chat(
    request: ChatRequest,
    rag_engine: RAGEngine = Depends(get_rag_engine),  # noqa: B008
) -> StreamingResponse:
    """Stream a response to the user message as Server-Sent Events.

    Retrieves relevant context from the vector store, builds an augmented prompt,
    and streams Claude's response token by token. The stream ends with [DONE].
    """
    return StreamingResponse(
        tokens_to_sse(rag_engine.stream_response(request.message, request.session_id)),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.delete("/chat/history")
async def clear_history(
    rag_engine: RAGEngine = Depends(get_rag_engine),  # noqa: B008
) -> StatusResponse:
    """Clear the in-memory conversation history for the default session."""
    rag_engine.clear_history()
    return StatusResponse(status="ok")
