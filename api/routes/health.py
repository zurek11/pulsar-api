"""Health check endpoint."""

from fastapi import APIRouter, Depends

from api.deps import get_rag_engine
from models.schemas import HealthResponse
from rag.engine import RAGEngine

router = APIRouter(prefix="/api")


@router.get("/health")
async def health(
    rag_engine: RAGEngine = Depends(get_rag_engine),  # noqa: B008
) -> HealthResponse:
    """Return API liveness and RAG readiness status.

    rag_ready reflects whether the vector store contains indexed documents.
    """
    return HealthResponse(status="ok", rag_ready=rag_engine.is_ready())
