# Pulsar API

## About

FastAPI backend for the Pulsar learning project. Handles chat communication with RAG pipeline and LLM (Claude) streaming responses. Serves as the brain behind [pulsar-chat](https://github.com/zurek11/pulsar-chat).

**⚠️ This is a PUBLIC repository.** Never commit secrets, API keys, .env files, or any sensitive data. The Anthropic API key lives in `.env` (gitignored) and is loaded via pydantic-settings.

- **Author:** Adam Žúrek (https://github.com/zurek11)
- **Repo:** https://github.com/zurek11/pulsar-api
- **Frontend:** https://github.com/zurek11/pulsar-chat

## Stack

- **Framework:** FastAPI (async)
- **Language:** Python 3.13+
- **Package Manager:** uv
- **LLM:** Anthropic Claude API (streaming)
- **RAG Framework:** LlamaIndex (starting simple, evolving through phases)
- **Vector Store:** ChromaDB (Phase 1) → Qdrant (Phase 2+)
- **Embeddings:** sentence-transformers (local) or Voyage AI
- **Testing:** pytest + pytest-asyncio + httpx
- **Linting & Formatting:** ruff
- **Type Checking:** mypy (strict)
- **Containerization:** Docker (multi-stage build with uv)
- **Server:** uvicorn (ASGI)

## Project Structure

```
api/
├── routes/         # FastAPI route handlers
│   ├── chat.py     # POST /api/chat (SSE stream), DELETE /api/chat/history
│   └── health.py   # GET /api/health
├── deps.py         # Dependency injection
└── middleware.py   # CORS, error handling
core/
├── config.py       # Settings via pydantic-settings (.env)
└── logging.py      # Structured logging setup
rag/
├── engine.py       # RAG orchestrator — query → retrieve → generate
├── ingest.py       # Document loading, chunking, embedding
├── retriever.py    # Vector store search strategies
└── prompts.py      # System prompts and prompt templates
llm/
├── client.py       # Anthropic Claude client wrapper
└── streaming.py    # SSE streaming helpers
models/
└── schemas.py      # Pydantic request/response schemas
main.py             # FastAPI app factory
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests (API + RAG)
└── conftest.py     # Shared fixtures
data/
└── documents/      # RAG knowledge base (PDF/MD files about RAG)
```

## Architecture & Decisions
 
See `ARCHITECTURE.md` for the full project vision, RAG pipeline design, internal architecture
diagrams, request flow, technology rationale, and development workflow.
Claude Code: read this file when working on cross-cutting concerns or when you need to
understand why a specific technology or pattern was chosen.

## Commands

- `uv sync --extra dev` — install all dependencies including dev tools (pytest, ruff, mypy)
- `uv sync` — install production dependencies only (no dev tools)
- `uv run uvicorn main:app --reload --port 8000` — start dev server
- `uv run pytest` — run all tests
- `uv run pytest tests/unit` — run unit tests only
- `uv run pytest tests/integration` — run integration tests
- `uv run ruff check .` — lint
- `uv run ruff format .` — format
- `uv run mypy .` — type checking

### Docker

- `docker build -t pulsar-api .` — build image
- `docker run -p 8000:8000 --env-file .env pulsar-api` — run container

### Document Ingestion
 
- `uv run python -m rag.ingest` — ingest all files from `data/documents/`

## Code Conventions

### Python

- Python 3.13+ features allowed (type hints, match statements, etc.)
- Type hints required on all functions (params + return)
- Async by default — use `async def` for route handlers and I/O operations
- Pydantic v2 for all data validation and settings
- No bare `except:` — always catch specific exceptions
- Docstrings on all public functions and classes

### FastAPI Patterns

- Route handlers in `api/routes/` — thin controllers, delegate to services
- Business logic in `rag/` and `llm/` — never in route handlers
- Dependencies via FastAPI `Depends()` — injected config, RAG engine, LLM client
- SSE streaming uses FastAPI's native `EventSourceResponse` (FastAPI 0.115+)

### Testing

- pytest with pytest-asyncio for async tests
- httpx `AsyncClient` for API integration tests
- Mock LLM calls in unit tests — never hit real Claude API
- Fixtures in `conftest.py` — shared across test modules
- Follow AAA pattern: Arrange, Act, Assert

### Project Layout

- Flat layout — modules at project root, importable as `from rag.engine import ...`
- No circular imports — dependency flow: routes → services → core
- Settings loaded from `.env` via `pydantic-settings`

## Git Workflow

### Commit Messages — Emoji Conventional Commits
```
🎉 feat: add RAG retrieval endpoint with streaming
🐛 fix: handle empty document collection gracefully
♻️ refactor: extract embedding logic into separate module
🧪 test: add integration tests for chat streaming
📝 docs: document RAG pipeline architecture
🔧 chore: update dependencies
🐳 docker: add health check to container
🚀 release: v0.2.0
```

### Branch Flow
 
Claude Code creates feature branches, pushes, and opens PRs. Adam reviews and merges.
 
- `main` — stable, versioned releases only
- `feat/[description]` — new features
- `fix/[description]` — bug fixes
- No develop branch. Feature branches → PR → main.

### PR Workflow
 
1. Create branch from main
2. Implement + write tests
3. Run: `uv run pytest && uv run ruff check . && uv run ruff format --check . && uv run mypy .`
4. Bump version (semver) + update CHANGELOG.md
5. Commit + push
6. Create PR titled "🚀 Release vX.Y.Z" with changelog in body
7. Add `zurek11` as reviewer
8. Adam reviews on GitHub — can tag `@claude` directly in PR for automatic fixes, or return to Claude Code locally

### Versioning
 
Semantic versioning in `pyproject.toml`. See `.claude/skills/release/SKILL.md` for details.

## Claude Code Configuration

### Skills (`.claude/skills/`)

Skills are NOT auto-applied. Claude Code MUST invoke each skill explicitly via the Skill tool
before the corresponding work begins. Skills are mandatory, not optional suggestions.
 
| Skill                | MUST invoke before…                                                |
| -------------------- | ------------------------------------------------------------------ |
| **fastapi-endpoint** | creating or modifying any route handler or SSE streaming code      |
| **rag-pipeline**     | working on ingestion, retrieval, embeddings, or prompt templates   |
| **testing**          | creating or modifying test files                                   |
| **git-workflow**     | any `git push` or `gh pr create`                                   |
| **release**          | bumping version in `pyproject.toml` or creating a PR to `main`     |
| **docker**           | editing the `Dockerfile` or any container config                   |

### Rules (`.claude/rules/`)
 
- **security.md** — public repo safety, API key handling (always active)

### Ignored (`.claudeignore`)
 
Claude Code skips: .venv, __pycache__, .env, data/chroma/, large PDFs, test artifacts.

## Important Notes
 
- Frontend (pulsar-chat) connects from `http://localhost:5173`
- API runs on `http://localhost:8000`
- Interactive API docs at `http://localhost:8000/docs`
- CORS is configured to allow frontend origin
- Chat history lives in memory (dict) — no database needed
- Anthropic API key goes in `.env` as `ANTHROPIC_API_KEY`
- RAG documents go in `data/documents/` — large files are gitignored
- GitHub CLI (`gh`) is used for PR creation from Claude Code
