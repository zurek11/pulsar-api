"""Unit tests for the RAG prompt builder."""

from anthropic.types import MessageParam

from llm.prompts import SYSTEM_PROMPT, build_prompt


def test_build_prompt_with_chunks() -> None:
    messages = build_prompt(
        query="What is RAG?",
        chunks=[
            "RAG stands for Retrieval-Augmented Generation.",
            "It combines retrieval with generation.",
        ],
        history=[],
    )
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    content = str(messages[0]["content"])
    assert "What is RAG?" in content
    assert "RAG stands for" in content


def test_build_prompt_no_chunks_fallback() -> None:
    messages = build_prompt(query="What is RAG?", chunks=[], history=[])
    assert "No relevant context" in str(messages[0]["content"])


def test_build_prompt_preserves_history() -> None:
    history: list[MessageParam] = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
    ]
    messages = build_prompt("Follow-up question", ["some context"], history)
    assert messages[0] == {"role": "user", "content": "Hello"}
    assert messages[1] == {"role": "assistant", "content": "Hi!"}
    assert messages[-1]["role"] == "user"
    assert "Follow-up question" in str(messages[-1]["content"])


def test_build_prompt_chunks_separated() -> None:
    messages = build_prompt("q", ["chunk A", "chunk B"], [])
    content = str(messages[0]["content"])
    assert "chunk A" in content
    assert "chunk B" in content


def test_system_prompt_not_empty() -> None:
    assert len(SYSTEM_PROMPT) > 50
