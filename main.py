"""Pulsar API — FastAPI application factory."""

from fastapi import FastAPI

from api.middleware import register_middleware
from api.routes import chat, health
from core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="Pulsar API",
    description="RAG pipeline + LLM orchestration backend for pulsar-chat.",
    version="0.1.1",
)

register_middleware(app)

app.include_router(health.router)
app.include_router(chat.router)
