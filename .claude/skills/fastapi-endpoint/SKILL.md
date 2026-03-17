---
name: fastapi-endpoint
description: Create new FastAPI endpoints with proper typing, SSE streaming, dependency injection, and error handling. Use when adding API routes or modifying endpoint behavior.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# FastAPI Endpoint Pattern

## When to Use
- Adding a new API endpoint
- Modifying existing endpoint behavior
- Implementing SSE streaming responses

## Streaming Endpoint Template

```python
from collections.abc import AsyncIterable
from fastapi import APIRouter, Depends
from fastapi.sse import EventSourceResponse, ServerSentEvent
from models.schemas import ChatRequest
from rag.engine import RAGEngine
from api.deps import get_rag_engine

router = APIRouter(prefix="/api")

@router.post("/chat", response_class=EventSourceResponse)
async def chat(
    request: ChatRequest,
    rag_engine: RAGEngine = Depends(get_rag_engine),
) -> AsyncIterable[ServerSentEvent]:
    async for token in rag_engine.stream_response(request.message):
        yield ServerSentEvent(data=token)
    yield ServerSentEvent(data="[DONE]")
```

## Non-Streaming Endpoint Template

```python
from fastapi import APIRouter
from models.schemas import StatusResponse

router = APIRouter(prefix="/api")

@router.delete("/chat/history")
async def clear_history() -> StatusResponse:
    # clear logic
    return StatusResponse(status="ok")
```

## Rules
1. Route handlers are thin — delegate to services in `rag/` or `llm/`
2. All request/response models in `models/schemas.py` (Pydantic v2)
3. Dependencies injected via `Depends()` — config, RAG engine, LLM client
4. SSE streaming uses FastAPI native `EventSourceResponse` + `ServerSentEvent`
5. Always handle errors — return proper HTTP status codes
6. Type hints on all params and return types
7. Async by default for all route handlers
