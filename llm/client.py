"""Anthropic Claude client — async streaming wrapper."""

import logging
from collections.abc import AsyncIterator

import anthropic
from anthropic.types import MessageParam

from core.config import get_settings

logger = logging.getLogger(__name__)

# Upper bound on generated tokens per response.
# Increase if you expect very long answers.
_MAX_TOKENS = 4096


class LLMClient:
    """Thin async wrapper around AsyncAnthropic for token-by-token streaming.

    Reads model name and API key from application settings so callers
    never touch credentials directly.
    """

    def __init__(self) -> None:
        """Initialise the Anthropic async client from application settings."""
        settings = get_settings()
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._model = settings.model_name
        logger.debug("LLMClient initialised with model '%s'", self._model)

    async def stream_response(
        self,
        messages: list[MessageParam],
        system: str = "",
    ) -> AsyncIterator[str]:
        """Stream text tokens from Claude.

        Args:
            messages: Conversation history in Anthropic message format
                      (alternating user / assistant turns).
            system: Optional system prompt injected before the conversation.

        Yields:
            Raw text tokens as they arrive from the API.

        Raises:
            anthropic.APIError: On any API-level failure (auth, rate-limit, etc.).
        """
        logger.debug("Streaming response from %s (%d messages)", self._model, len(messages))
        async with self._client.messages.stream(
            model=self._model,
            max_tokens=_MAX_TOKENS,
            system=system,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text
