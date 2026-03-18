"""Unit tests for Pydantic request/response schemas."""

from models.schemas import ChatRequest, HealthResponse, StatusResponse


def test_chat_request_defaults() -> None:
    req = ChatRequest(message="hello")
    assert req.message == "hello"
    assert req.session_id == "default"


def test_chat_request_custom_session() -> None:
    req = ChatRequest(message="hello", session_id="user-123")
    assert req.session_id == "user-123"


def test_health_response_ready() -> None:
    resp = HealthResponse(status="ok", rag_ready=True)
    assert resp.status == "ok"
    assert resp.rag_ready is True


def test_health_response_not_ready() -> None:
    resp = HealthResponse(status="ok", rag_ready=False)
    assert resp.rag_ready is False


def test_status_response() -> None:
    resp = StatusResponse(status="ok")
    assert resp.status == "ok"
