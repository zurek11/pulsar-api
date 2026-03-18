"""SSE streaming helpers — format LLM token streams for HTTP clients."""

from collections.abc import AsyncIterator


async def tokens_to_sse(token_stream: AsyncIterator[str]) -> AsyncIterator[bytes]:
    """Convert a text-token stream into SSE-formatted byte chunks.

    Each token is wrapped as::

        data: <token>\\n\\n

    A final sentinel is appended after the stream is exhausted::

        data: [DONE]\\n\\n

    Args:
        token_stream: Async iterator of raw text tokens (from LLMClient).

    Yields:
        UTF-8 encoded SSE frames ready to be sent over an HTTP response.
    """
    async for token in token_stream:
        yield f"data: {token}\n\n".encode()
    yield b"data: [DONE]\n\n"
