"""RAG orchestrator — retrieval, prompt building, and LLM streaming."""

import logging
from collections.abc import AsyncIterator

from anthropic.types import MessageParam

from core.config import Settings
from llm.client import LLMClient
from llm.prompts import SYSTEM_PROMPT, build_prompt
from rag.retriever import Retriever

logger = logging.getLogger(__name__)


class RAGEngine:
    """Orchestrates retrieval-augmented generation.

    Owns a Retriever and LLMClient. Manages per-session chat history in memory
    (single process, no persistence across restarts by design — Phase 1).
    """

    def __init__(self, settings: Settings) -> None:
        """Initialise retriever and LLM client from application settings."""
        self._retriever = Retriever(
            persist_dir=settings.chroma_persist_dir,
            collection_name=settings.chroma_collection_name,
            embedding_model=settings.embedding_model,
        )
        self._llm = LLMClient()
        self._top_k = settings.top_k
        self._history: dict[str, list[MessageParam]] = {}
        logger.info("RAGEngine initialised (top_k=%d)", self._top_k)

    def is_ready(self) -> bool:
        """Return True if the vector store contains indexed documents."""
        return self._retriever.is_ready()

    def clear_history(self, session_id: str = "default") -> None:
        """Clear conversation history for the given session.

        Args:
            session_id: Session identifier to clear.
        """
        self._history[session_id] = []

    async def stream_response(
        self,
        message: str,
        session_id: str = "default",
    ) -> AsyncIterator[str]:
        """Retrieve context, build prompt, and stream Claude's response token by token.

        Saves to history only after the full response is received, so a failed
        or interrupted stream does not pollute the conversation history.

        Args:
            message: The user's question.
            session_id: Session identifier for conversation history.

        Yields:
            Raw text tokens from Claude. Caller handles SSE framing and [DONE].
        """
        history = self._history.setdefault(session_id, [])

        nodes = await self._retriever.retrieve(message, self._top_k)
        chunks = [node.get_content() for node in nodes]
        logger.debug("Building prompt with %d chunk(s) for session '%s'", len(chunks), session_id)

        messages = build_prompt(message, chunks, history)
        full_response: list[str] = []

        async for token in self._llm.stream_response(messages, system=SYSTEM_PROMPT):
            full_response.append(token)
            yield token

        # Persist to history using the original message (not the context-augmented version)
        # so subsequent turns don't bloat with repeated retrieved text.
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "".join(full_response)})
