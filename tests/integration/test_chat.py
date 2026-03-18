"""Integration tests for POST /api/chat and DELETE /api/chat/history."""

from collections.abc import AsyncIterator, Generator
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from api.deps import get_rag_engine
from main import app


async def _token_stream(*tokens: str) -> AsyncIterator[str]:
    """Async generator that yields the given tokens — used as a stream_response mock."""
    for token in tokens:
        yield token


@pytest.fixture(autouse=True)
def mock_engine() -> Generator[MagicMock]:
    """Replace the RAGEngine singleton with a mock for every test in this module."""
    engine = MagicMock()
    # side_effect creates a fresh async generator on every call to stream_response.
    engine.stream_response.side_effect = lambda msg, sid="default": _token_stream("Hello", " world")
    app.dependency_overrides[get_rag_engine] = lambda: engine
    yield engine
    app.dependency_overrides.clear()


async def test_chat_returns_200(client: AsyncClient) -> None:
    async with client.stream("POST", "/api/chat", json={"message": "What is RAG?"}) as response:
        assert response.status_code == 200


async def test_chat_content_type(client: AsyncClient) -> None:
    async with client.stream("POST", "/api/chat", json={"message": "hello"}) as response:
        assert "text/event-stream" in response.headers["content-type"]


async def test_chat_sse_ends_with_done(client: AsyncClient) -> None:
    async with client.stream("POST", "/api/chat", json={"message": "hello"}) as response:
        chunks: list[str] = []
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                chunks.append(line[6:])
    assert len(chunks) > 0
    assert chunks[-1] == "[DONE]"


async def test_chat_streams_tokens(client: AsyncClient) -> None:
    async with client.stream("POST", "/api/chat", json={"message": "hello"}) as response:
        tokens: list[str] = []
        async for line in response.aiter_lines():
            if line.startswith("data: ") and line != "data: [DONE]":
                tokens.append(line[6:])
    assert "Hello" in tokens
    assert " world" in tokens


async def test_chat_default_session_id(client: AsyncClient, mock_engine: MagicMock) -> None:
    async with client.stream("POST", "/api/chat", json={"message": "hi"}) as response:
        async for _ in response.aiter_lines():
            pass
    mock_engine.stream_response.assert_called_once_with("hi", "default")


async def test_chat_custom_session_id(client: AsyncClient, mock_engine: MagicMock) -> None:
    async with client.stream(
        "POST", "/api/chat", json={"message": "hi", "session_id": "user-42"}
    ) as response:
        async for _ in response.aiter_lines():
            pass
    mock_engine.stream_response.assert_called_once_with("hi", "user-42")


async def test_clear_history_returns_ok(client: AsyncClient) -> None:
    response = await client.delete("/api/chat/history")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_clear_history_calls_engine(client: AsyncClient, mock_engine: MagicMock) -> None:
    await client.delete("/api/chat/history")
    mock_engine.clear_history.assert_called_once()
