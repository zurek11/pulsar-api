"""Chat endpoints — POST /api/chat (SSE stream) and DELETE /api/chat/history."""

import asyncio
from collections.abc import AsyncIterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.schemas import ChatRequest, StatusResponse

router = APIRouter(prefix="/api")

# In-memory chat history — single session, no persistence needed.
_chat_history: list[dict[str, str]] = []

# Canned response used by the mockup until the RAG pipeline is wired up.
_MOCK_RESPONSE = (
    "This is a mock response. "
    "The RAG pipeline is not yet connected. "
    "Once implemented, I will retrieve relevant context from the knowledge base "
    "and generate a grounded answer using Claude."
)


async def _mock_token_stream(message: str) -> AsyncIterator[str]:
    """Yield tokens from a canned response, simulating LLM streaming."""
    _chat_history.append({"role": "user", "content": message})
    full_response: list[str] = []

    for word in _MOCK_RESPONSE.split(" "):
        token = word + " "
        full_response.append(token)
        yield token
        await asyncio.sleep(0.05)

    _chat_history.append({"role": "assistant", "content": "".join(full_response).strip()})
    yield "[DONE]"


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """Stream a response to the user message as Server-Sent Events.

    Each chunk is emitted as:
        data: <token>\\n\\n

    The stream ends with:
        data: [DONE]\\n\\n
    """

    async def event_generator() -> AsyncIterator[bytes]:
        async for token in _mock_token_stream(request.message):
            yield f"data: {token}\n\n".encode()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.delete("/chat/history")
async def clear_history() -> StatusResponse:
    """Clear the in-memory conversation history."""
    _chat_history.clear()
    return StatusResponse(status="ok")
