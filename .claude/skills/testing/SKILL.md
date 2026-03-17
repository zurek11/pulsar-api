---
name: testing
description: Write pytest tests for FastAPI endpoints, RAG pipeline, and async code. Use when creating tests, fixing test failures, or adding test coverage.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(uv:*), Bash(pytest:*)
---

# Testing Patterns

## When to Use
- Writing tests for a new endpoint or RAG component
- Fixing failing tests
- Adding test coverage

## API Integration Test

```python
# tests/integration/test_chat.py
from httpx import ASGITransport, AsyncClient
from main import app
import pytest

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

async def test_chat_streams_response(client: AsyncClient):
    async with client.stream(
        "POST",
        "/api/chat",
        json={"message": "What is RAG?"},
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

        chunks = []
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                chunks.append(line[6:])

        assert len(chunks) > 0
        assert chunks[-1] == "[DONE]"

async def test_clear_history(client: AsyncClient):
    response = await client.delete("/api/chat/history")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

async def test_health(client: AsyncClient):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

## Unit Test (RAG Component)

```python
# tests/unit/test_retriever.py
from rag.retriever import retrieve

def test_retrieve_returns_relevant_chunks(mock_index):
    results = retrieve(mock_index, "What is chunking?", top_k=3)
    assert len(results) <= 3
    assert all(isinstance(r, str) for r in results)
```

## Rules
1. Unit tests: `tests/unit/` — test functions and classes in isolation
2. Integration tests: `tests/integration/` — test API endpoints with httpx
3. Shared fixtures in `tests/conftest.py`
4. Mock LLM calls — never hit real Claude API in tests
5. No `@pytest.mark.asyncio` needed — `asyncio_mode = "auto"` in `pyproject.toml`
6. Follow AAA pattern: Arrange, Act, Assert
7. Run `uv run pytest` to execute all tests
