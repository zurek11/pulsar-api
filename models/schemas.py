"""Pydantic request/response schemas for pulsar-api."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Incoming chat message from the frontend."""

    message: str


class StatusResponse(BaseModel):
    """Generic status response."""

    status: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    rag_ready: bool
