"""FastAPI dependency providers for pulsar-api."""

from functools import lru_cache

from fastapi import Depends

from core.config import Settings, get_settings
from rag.engine import RAGEngine

# Re-export so routes import from a single place
__all__ = ["get_settings", "provide_settings", "get_rag_engine"]


def provide_settings(settings: Settings = Depends(get_settings)) -> Settings:  # noqa: B008
    """Inject application settings into route handlers."""
    return settings


@lru_cache
def get_rag_engine() -> RAGEngine:
    """Return a singleton RAGEngine, constructed once on first call.

    Using lru_cache means the engine (and its ChromaDB connection + embedding
    model) is initialised once at startup and reused across all requests.
    Call get_rag_engine.cache_clear() in tests to reset.
    """
    return RAGEngine(get_settings())
