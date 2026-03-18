"""Integration tests for GET /api/health."""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from api.deps import get_rag_engine
from main import app


@pytest.fixture(autouse=True)
def mock_engine() -> Generator[MagicMock]:
    """Replace the RAGEngine singleton with a mock for every test in this module."""
    engine = MagicMock()
    engine.is_ready.return_value = True
    app.dependency_overrides[get_rag_engine] = lambda: engine
    yield engine
    app.dependency_overrides.clear()


async def test_health_returns_200(client: AsyncClient) -> None:
    response = await client.get("/api/health")
    assert response.status_code == 200


async def test_health_response_schema(client: AsyncClient) -> None:
    response = await client.get("/api/health")
    data = response.json()
    assert data["status"] == "ok"
    assert "rag_ready" in data


async def test_health_rag_ready_true(client: AsyncClient) -> None:
    response = await client.get("/api/health")
    assert response.json()["rag_ready"] is True


async def test_health_rag_not_ready(client: AsyncClient, mock_engine: MagicMock) -> None:
    mock_engine.is_ready.return_value = False
    response = await client.get("/api/health")
    assert response.json()["rag_ready"] is False
