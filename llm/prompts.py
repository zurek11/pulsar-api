"""System prompt and prompt builder for the RAG pipeline."""

from anthropic.types import MessageParam

SYSTEM_PROMPT = """You are a knowledgeable assistant specialising in space engineering, \
astrophysics, and related sciences.

Answer questions using the retrieved context provided in each message. \
When you use information from the context, cite the source naturally in your response.

If the context does not contain enough information to answer confidently, say so clearly \
— do not fabricate facts or extrapolate beyond what the sources support.

Be concise, precise, and helpful."""


def build_prompt(
    query: str,
    chunks: list[str],
    history: list[MessageParam],
) -> list[MessageParam]:
    """Build the messages list for the Claude API call.

    Injects retrieved context into the current user turn only — history is kept
    clean (original questions without context) so subsequent turns stay concise.

    Args:
        query: The user's current question.
        chunks: Retrieved text chunks from the vector store.
        history: Previous conversation turns (alternating user / assistant).

    Returns:
        Full messages list ready to pass to LLMClient.stream_response().
    """
    if chunks:
        context = "\n\n---\n\n".join(chunks)
    else:
        context = "No relevant context was found in the knowledge base."

    user_content = f"<context>\n{context}\n</context>\n\nQuestion: {query}"

    return [
        *history,
        {"role": "user", "content": user_content},
    ]
