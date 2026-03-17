# 🌟 Pulsar API

FastAPI backend with RAG pipeline and LLM streaming for the Pulsar learning project.

> **Learning project** — Built to learn RAG systems end-to-end by building them. Not intended for production use.

## What is this?

Pulsar API is the backend part of a two-repo learning project:

- **[pulsar-chat](https://github.com/zurek11/pulsar-chat)** — SvelteKit chat interface with streaming responses
- **[pulsar-api](https://github.com/zurek11/pulsar-api)** (this repo) — FastAPI backend with RAG pipeline and LLM integration

Ask questions → RAG retrieves relevant documents → Claude generates grounded answers → streamed back in real-time.

## Stack

| Layer         | Technology                        |
| ------------- | --------------------------------- |
| Framework     | FastAPI (async)                   |
| Language      | Python 3.13+                      |
| Package Mgr   | uv                               |
| LLM           | Anthropic Claude (streaming)     |
| RAG           | LlamaIndex                       |
| Vector Store  | ChromaDB → Qdrant                |
| Embeddings    | sentence-transformers             |
| Testing       | pytest + httpx                    |
| Lint & Format | ruff                              |
| Type Check    | mypy (strict)                     |
| Container     | Docker (multi-stage with uv)      |

## Getting Started

### Local Development

```bash
# Prerequisites: Python 3.13+, uv (https://docs.astral.sh/uv/)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/zurek11/pulsar-api.git
cd pulsar-api
uv sync --extra dev   # includes pytest, ruff, mypy — use plain `uv sync` for prod

# Configure
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Ingest RAG documents (put PDFs/MDs in data/documents/ first)
uv run python -m rag.ingest

# Start dev server
uv run uvicorn main:app --reload --port 8000
```

### Docker

```bash
# Just the API
docker build -t pulsar-api .
docker run -p 8000:8000 --env-file .env pulsar-api

# Full stack (chat + api)
# Run from pulsar-chat repo:
docker compose up
```

## API Endpoints

| Method   | Path                | Description                         |
| -------- | ------------------- | ----------------------------------- |
| `POST`   | `/api/chat`         | Send message, get SSE streamed response |
| `DELETE` | `/api/chat/history` | Clear conversation history          |
| `GET`    | `/api/health`       | Health check (includes RAG status)  |

Interactive docs: http://localhost:8000/docs

## Development

```bash
uv run uvicorn main:app --reload    # Dev server (port 8000)
uv run pytest                            # All tests
uv run pytest tests/unit                 # Unit tests only
uv run pytest tests/integration          # Integration tests only
uv run ruff check .                      # Lint
uv run ruff format .                     # Format
uv run mypy .                            # Type checking
```

## RAG Knowledge Base

Put PDF or Markdown files in `data/documents/`. The meta-strategy: **the knowledge base contains documents about RAG itself** — papers, docs, tutorials. We learn RAG by asking our RAG system about RAG.

## What I Learned

_This section will be updated as the project progresses._

- [ ] FastAPI SSE streaming with EventSourceResponse
- [ ] RAG pipeline: ingest → chunk → embed → store → retrieve → generate
- [ ] LlamaIndex document loaders and query engines
- [ ] ChromaDB vector store operations
- [ ] Anthropic Python SDK streaming
- [ ] pytest-asyncio for async API testing
- [ ] uv package management
- [ ] pydantic-settings for configuration
- [ ] Docker multi-stage builds with uv

## License

MIT