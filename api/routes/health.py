"""Health check endpoint."""

from fastapi import APIRouter

from models.schemas import HealthResponse

router = APIRouter(prefix="/api")


@router.get("/health")
async def health() -> HealthResponse:
    """Return API liveness and RAG readiness status.

    rag_ready will be False until the RAG pipeline is wired up (Phase 1).
    """
    return HealthResponse(status="ok", rag_ready=False)
