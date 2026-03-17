# Architecture & Vision

> This document captures the big picture for pulsar-api — the RAG backend powering the Pulsar
> learning project. Claude Code should read this when working on anything that touches architecture,
> cross-repo concerns, or when it needs to understand the "why" behind a technical choice.

## Why This Project Exists

Pulsar is a **learning project** with three parallel goals:

1. **Learn RAG end-to-end** — not by reading tutorials, but by building a complete retrieval-augmented generation system from scratch. Chunking, embeddings, vector stores, retrieval strategies, re-ranking, evaluation — the full pipeline.

2. **Learn Svelte 5 & modern frontend** — coming from a Python/backend background (FastAPI, AWS, distributed systems), this is an opportunity to build real frontend skills with the latest tools: SvelteKit, Svelte 5 runes, Tailwind CSS 4, Bun.

3. **Learn Anthropic tooling** — Claude Code, Claude Chat, Cowork, CLAUDE.md, skills, MCP integrations. Use the tools to build the project, and learn the tools by building the project.

The meta-strategy: **the RAG knowledge base will contain documents about RAG itself**. We learn RAG by asking our RAG system questions about RAG. When retrieval fails, we immediately understand why — because we know the source material.

## System Overview

The project is split into two repositories that work together:

```mermaid
graph TB
    subgraph "pulsar-chat (separate repo)"
        FE[SvelteKit + Svelte 5]
        FE -->|user message| API_CALL[fetch + ReadableStream]
    end

    subgraph "pulsar-api (this repo)"
        BE[FastAPI]
        RAG[RAG Pipeline]
        VDB[(Vector Store)]
        LLM[Claude API]

        BE -->|query| RAG
        RAG -->|semantic search| VDB
        RAG -->|augmented prompt| LLM
        LLM -->|streaming tokens| BE
    end

    API_CALL -->|POST /api/chat SSE| BE
    BE -->|streamed response| API_CALL

    subgraph "Knowledge Base"
        DOCS[PDF/MD documents about RAG]
        DOCS -->|chunked + embedded| VDB
    end
```

| Repo            | Purpose                          | Stack                                                                    |
| --------------- | -------------------------------- | ------------------------------------------------------------------------ |
| **pulsar-chat** | Chat UI with streaming           | SvelteKit, Svelte 5, Tailwind 4, Bun, TypeScript                         |
| **pulsar-api**  | RAG pipeline + LLM orchestration | Python, FastAPI, LlamaIndex, ChromaDB → Qdrant, Anthropic SDK            |

### Why Two Repos?

- Different languages (TypeScript vs Python) with different toolchains, linters, and test runners
- Independent deployment — frontend is a static build, backend is a Python service
- Clean separation of concerns — frontend knows nothing about RAG internals
- Both are Dockerized — each repo ships its own image

## Internal Architecture

```mermaid
graph TD
    subgraph "api/"
        ROUTES["routes/chat.py\nroutes/health.py"]
        DEPS["deps.py\nDependency injection"]
        MW["middleware.py\nCORS, errors"]
    end

    subgraph "rag/"
        ENGINE["engine.py\nRAG orchestrator"]
        INGEST["ingest.py\nDoc loading + chunking"]
        RETRIEVER["retriever.py\nVector search"]
        PROMPTS["prompts.py\nPrompt templates"]
    end

    subgraph "llm/"
        CLIENT["client.py\nAnthropic wrapper"]
        STREAM["streaming.py\nSSE helpers"]
    end

    subgraph "core/"
        CONFIG["config.py\nSettings from .env"]
        LOG["logging.py"]
    end

    subgraph "models/"
        SCHEMAS["schemas.py\nPydantic models"]
    end

    subgraph "External"
        VDB[(ChromaDB / Qdrant)]
        CLAUDE["Claude API"]
        FRONTEND["pulsar-chat\nlocalhost:5173"]
    end

    FRONTEND -->|HTTP| ROUTES
    ROUTES --> DEPS
    ROUTES --> SCHEMAS
    DEPS --> ENGINE
    DEPS --> CONFIG
    ENGINE --> RETRIEVER
    ENGINE --> PROMPTS
    ENGINE --> CLIENT
    RETRIEVER --> VDB
    CLIENT --> CLAUDE
    CLIENT --> STREAM
    INGEST --> VDB

    style ROUTES fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style DEPS fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style MW fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style ENGINE fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style INGEST fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style RETRIEVER fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style PROMPTS fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style CLIENT fill:#E1F5EE,stroke:#0F6E56,color:#085041
    style STREAM fill:#E1F5EE,stroke:#0F6E56,color:#085041
    style CONFIG fill:#F1EFE8,stroke:#5F5E5A,color:#444441
    style SCHEMAS fill:#F1EFE8,stroke:#5F5E5A,color:#444441
    style VDB fill:#FAECE7,stroke:#993C1D,color:#712B13
    style CLAUDE fill:#FAECE7,stroke:#993C1D,color:#712B13
    style FRONTEND fill:#FAECE7,stroke:#993C1D,color:#712B13
```

### Dependency Flow

```
routes (thin handlers) → deps (injection) → engine (orchestration) → retriever + llm client → external services
```

No circular imports. Routes never import from `rag` directly — always through `deps.py`.

## API Contract

### Endpoints

| Method | Path                | Description                         | Request                    | Response                                              |
| ------ | ------------------- | ----------------------------------- | -------------------------- | ----------------------------------------------------- |
| POST   | `/api/chat`         | Send message, get streamed response | `{ "message": "string" }`  | SSE stream: `data: token\n\n` ... `data: [DONE]\n\n`  |
| DELETE | `/api/chat/history` | Clear conversation history          | —                          | `{ "status": "ok" }`                                  |
| GET    | `/api/health`       | Health check                        | —                          | `{ "status": "ok", "rag_ready": bool }`               |

### SSE Stream Format

```
data: Hello
data:  there
data: ,
data:  how can I help?
data: [DONE]
```

Each `data:` line contains one or more tokens. The frontend reads these via `ReadableStream` and
appends them to the current assistant message in real-time.

### Request Flow

```mermaid
sequenceDiagram
    participant FE as pulsar-chat
    participant API as FastAPI Router
    participant RAG as RAG Engine
    participant VS as Vector Store
    participant LLM as Claude API

    FE->>API: POST /api/chat {"message": "What is chunking in RAG?"}
    API->>RAG: query(message, chat_history)
    RAG->>VS: semantic_search(embedding(message), top_k=5)
    VS-->>RAG: [relevant chunks]
    RAG->>RAG: build_prompt(message, chunks, history)
    RAG->>LLM: stream(augmented_prompt)

    loop token by token
        LLM-->>RAG: token
        RAG-->>API: yield token
        API-->>FE: data: token
    end

    LLM-->>RAG: end of stream
    RAG-->>API: yield [DONE]
    API-->>FE: data: [DONE]

    Note over FE,LLM: Clear history flow
    FE->>API: DELETE /api/chat/history
    API->>RAG: clear_history()
    API-->>FE: {"status": "ok"}
```

## RAG Pipeline Design

### Phase 1: Naive RAG (current target)

```mermaid
graph LR
    subgraph "Ingestion (offline)"
        DOCS["PDF/MD files"] --> CHUNK["Chunking\n512 tokens\n50 overlap"]
        CHUNK --> EMBED["Embedding\nall-MiniLM-L6-v2"]
        EMBED --> STORE["ChromaDB"]
    end

    subgraph "Query (real-time)"
        QUERY["User query"] --> QEMBED["Embed query"]
        QEMBED --> SEARCH["Top-5 similarity"]
        SEARCH --> STORE
        STORE --> CONTEXT["Retrieved chunks"]
        CONTEXT --> PROMPT["Augmented prompt"]
        PROMPT --> LLM["Claude\nstreaming"]
        LLM --> RESPONSE["SSE tokens"]
    end
```

Components:

- **Document loader:** PyMuPDF for PDFs, plain read for Markdown
- **Chunking:** LlamaIndex `SentenceSplitter` (recursive character splitter)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (local, free, fast)
- **Vector store:** ChromaDB (in-memory or persistent, zero external deps)
- **LLM:** Claude via Anthropic Python SDK (streaming)
- **Prompt template:** System prompt with retrieved context + conversation history

### Phase 2: Hybrid Retrieval (weeks 3-4)

- Add BM25 lexical search alongside semantic search
- Two-stage retrieval: broad fetch (top-50) → cross-encoder re-ranking (top-5)
- Metadata filtering (source, date, category)
- Experiment with chunking strategies: semantic chunking, parent-child chunks

### Phase 3: Agentic RAG (weeks 5-6)

- LLM agent decides when and what to retrieve (tool-use pattern)
- Query reformulation — agent rewrites vague queries before searching
- Multi-step retrieval loops with validation
- LangGraph for stateful agent workflows

### Phase 4: Evaluation (ongoing)

- RAGAs framework — faithfulness, answer relevancy, context precision
- Build eval dataset from the knowledge base
- Automated regression testing for retrieval quality
- A/B testing different retrieval strategies

```mermaid
graph LR
    P1[Phase 1\nNaive RAG] --> P2[Phase 2\nHybrid Retrieval]
    P2 --> P3[Phase 3\nAgentic RAG]
    P3 --> P4[Phase 4\nEvaluation]

    style P1 fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style P2 fill:#E1F5EE,stroke:#0F6E56,color:#085041
    style P3 fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style P4 fill:#FAECE7,stroke:#993C1D,color:#712B13
```

### Dataset

The knowledge base consists of **documents about RAG itself**:

- Research papers (Lewis et al. 2020 original RAG paper, etc.)
- Framework documentation (LlamaIndex, LangChain)
- Blog posts and tutorials about RAG patterns
- Evaluation methodology papers

This creates a recursive learning loop — when the RAG system fails to answer a question about RAG, we immediately understand what went wrong because we know the source material.

## Key Code Patterns

### Configuration (pydantic-settings)

```python
# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    model_name: str = "claude-sonnet-4-6"
    chroma_persist_dir: str = "./data/chroma"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 5
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173"

    model_config = {"env_file": ".env"}
```

### Dependency Injection

```python
# api/deps.py
from functools import lru_cache
from core.config import Settings
from rag.engine import RAGEngine

@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_rag_engine(settings: Settings = Depends(get_settings)) -> RAGEngine:
    return RAGEngine(settings)
```

### Chat History (in-memory)

```python
# Simple in-memory store — no database needed
_chat_history: dict[str, list[dict[str, str]]] = {"default": []}

def get_history(session_id: str = "default") -> list[dict[str, str]]:
    return _chat_history.setdefault(session_id, [])

def clear_history(session_id: str = "default") -> None:
    _chat_history[session_id] = []
```

No database, no persistence across restarts. This is intentional — complexity budget goes to RAG, not user management.

## Technology Decisions

### Why LlamaIndex (not LangChain)?

- Better document ingestion and indexing out of the box
- More opinionated about retrieval strategies (less boilerplate)
- Cleaner abstraction for "query engine" pattern
- Naive RAG in ~15 lines vs ~40 in LangChain
- Can always drop down to raw components when needed
- For Phase 3 (agentic), LangGraph will be added alongside

### Why uv (not pip/poetry)?

- Fastest Python package manager available (10-100x faster than pip)
- Built-in virtual environment management (`uv sync` creates .venv automatically)
- Lock file (`uv.lock`) for reproducible builds
- Drop-in replacement for pip workflows
- Same philosophy as Bun for JS — fast, modern, all-in-one

### Why FastAPI's native SSE (not sse-starlette)?

- FastAPI 0.115+ has built-in `EventSourceResponse` with `ServerSentEvent`
- Handles keep-alive pings, cache headers, proxy buffering automatically
- No extra dependency needed
- Pydantic model support out of the box

### Why ChromaDB first?

- Zero infrastructure — runs in-process, Python-native
- Perfect for learning and prototyping
- Easy migration path to Qdrant when ready for production features
- Persistent storage with a single flag change

### Why sentence-transformers locally?

- Free — no API costs during development
- Fast — runs on CPU, sub-second for single queries
- Good enough for learning — `all-MiniLM-L6-v2` is a solid baseline
- Can switch to Voyage AI or OpenAI embeddings later

### Why Docker?

- Reproducible environments across dev machines
- `docker compose up` runs the full stack (chat + api) with one command
- Foundation for future CI/CD pipeline
- Production-like setup from day one

## Development Workflow

### Feature Lifecycle

```mermaid
graph TD
    START((Start)) --> BRANCH["🌿 Create branch\nfeat/description"]
    BRANCH --> CODE["🎉 Implement\ncode + tests"]
    CODE --> TEST["🧪 Run tests\nuv run pytest"]
    TEST --> CHECK["✅ Run checks\nruff check · ruff format · mypy"]
    CHECK --> VERSION["🚀 Bump version\nsemver + CHANGELOG.md"]
    VERSION --> COMMIT["📤 Commit + push\nemoji conventional commit"]
    COMMIT --> PR["📋 Create PR via gh CLI\n🚀 Release vX.Y.Z — Nickname"]

    PR --> REVIEW{"👀 Adam reviews\non GitHub"}
    REVIEW -->|changes needed| FIX["🔄 Fix via @claude\nin PR or Claude Code locally"]
    FIX --> REVIEW
    REVIEW -->|approved| MERGE["✅ Merge to main"]
    MERGE --> TAG["🏷️ git tag vX.Y.Z"]
    TAG --> DONE((Done))

    style START fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style BRANCH fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style CODE fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style TEST fill:#E1F5EE,stroke:#0F6E56,color:#085041
    style CHECK fill:#FAEEDA,stroke:#854F0B,color:#633806
    style VERSION fill:#FAECE7,stroke:#993C1D,color:#712B13
    style COMMIT fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style PR fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style REVIEW fill:#FAEEDA,stroke:#854F0B,color:#633806
    style FIX fill:#FAECE7,stroke:#993C1D,color:#712B13
    style MERGE fill:#E1F5EE,stroke:#0F6E56,color:#085041
    style TAG fill:#F1EFE8,stroke:#5F5E5A,color:#444441
    style DONE fill:#E1F5EE,stroke:#0F6E56,color:#085041
```

### Roles

| Step                                                      | Who                                                 | Tool                       |
| --------------------------------------------------------- | --------------------------------------------------- | -------------------------- |
| Branch, implement, test, check, version, commit, push, PR | Claude Code                                         | Terminal / WebStorm plugin |
| Code review                                               | Adam                                                | GitHub PR interface        |
| Fix review comments                                       | Claude (via `@claude` in PR) or Claude Code locally | GitHub App / Terminal      |
| Approve + merge + tag                                     | Adam                                                | GitHub                     |

### PR Review with @claude on GitHub

When Adam leaves review comments on a PR, he can tag `@claude` directly in the comment.
The Claude GitHub App will read the feedback, make the fix, and push a commit to the PR branch automatically.
This avoids switching back to the terminal for minor fixes.

For larger changes, Adam returns to Claude Code locally, reads the review with `gh pr view --comments`,
and works through the feedback interactively.

## Future Considerations

Things we explicitly decided NOT to do yet, but might revisit:

- **CI/CD** — no pipeline yet. Docker images are built locally. Will set up GitHub Actions when there's a deployment target.
- **Authentication** — not needed for a local learning project. If this ever goes beyond localhost, add it.
- **Database** — not needed now. If chat history needs persistence, SQLite via SQLModel.
- **Rate limiting** — not needed for single user.
- **Caching** — embed query cache could help in Phase 2.
- **Observability** — LangWatch or LangSmith for RAG tracing in Phase 4.
- **Multiple conversations** — single chat thread only. No conversation list, no tabs.
- **Deployment** — no hosting planned. Everything runs on localhost via Docker.
