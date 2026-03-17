---
name: rag-pipeline
description: RAG components — document ingestion, chunking, embedding, retrieval, and generation. Use when building or modifying the RAG pipeline, adding new retrieval strategies, or changing document processing.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(uv:*), Bash(python:*)
---

# RAG Pipeline Patterns

## When to Use
- Adding or modifying document ingestion
- Changing chunking strategy
- Implementing new retrieval approaches
- Modifying prompt templates
- Integrating new embedding models

## Ingestion Pattern

```python
# rag/ingest.py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

def ingest_documents(
    data_dir: str = "data/documents",
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> VectorStoreIndex:
    documents = SimpleDirectoryReader(data_dir).load_data()
    parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    return index
```

## Retrieval Pattern

```python
# rag/retriever.py
from llama_index.core import VectorStoreIndex

def retrieve(
    index: VectorStoreIndex,
    query: str,
    top_k: int = 5,
) -> list[str]:
    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)
    return [node.get_content() for node in nodes]
```

## RAG Engine Pattern

```python
# rag/engine.py
from collections.abc import AsyncGenerator

class RAGEngine:
    async def stream_response(
        self,
        message: str,
        session_id: str = "default",
    ) -> AsyncGenerator[str, None]:
        # 1. Retrieve relevant chunks
        context_chunks = self.retrieve(message)

        # 2. Build augmented prompt
        prompt = self.build_prompt(message, context_chunks, session_id)

        # 3. Stream LLM response
        async for token in self.llm_client.stream(prompt):
            yield token

        # 4. Save to chat history
        self.save_to_history(session_id, message, collected_response)
```

## Rules
1. RAG components live in `rag/` — engine, ingest, retriever, prompts
2. LLM client lives in `llm/` — separate from RAG logic
3. Document files go in `data/documents/` (gitignored for large files)
4. Chunking params are configurable via settings (not hardcoded)
5. Always log retrieval results for debugging
6. Prompt templates in `src/rag/prompts.py` — not inline strings
7. Chat history passed to LLM for conversational context
