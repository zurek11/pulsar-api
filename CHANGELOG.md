# Changelog

All notable changes to Pulsar API — the RAG-powered backend for the Pulsar learning project.

## [0.3.0] — 2026-03-18 — "Signal Acquired"

The RAG pipeline is real. Ask it about space propulsion, Mars colonisation, or Starlink
and it reaches into the knowledge base, pulls the relevant chunks, and streams back a
grounded answer courtesy of Claude. Phase 1 is done — the signal is no longer hollow.

### 🎉 Added

- `scripts/download_dataset.py` — fetches 10 arXiv space engineering papers into `data/documents/`
- `rag/ingest.py` — full ingestion pipeline: `SimpleDirectoryReader` → `SentenceSplitter` (512 tokens, 50 overlap) → `HuggingFaceEmbedding` → ChromaDB persistent store; runnable via `python -m rag.ingest`
- `rag/retriever.py` — `Retriever` class: loads existing ChromaDB index, async top-k semantic search via `asyncio.to_thread`
- `rag/engine.py` — `RAGEngine`: the orchestrator; retrieves context, builds prompt, streams Claude, owns per-session in-memory history
- `llm/client.py` — `LLMClient`: async wrapper around `anthropic.AsyncAnthropic` with token streaming
- `llm/streaming.py` — `tokens_to_sse()`: converts token stream → SSE byte frames with `[DONE]` sentinel
- `llm/prompts.py` — `SYSTEM_PROMPT` (space engineering domain) + `build_prompt()` with context injection and clean history (no bloat from repeated retrieved text)
- `api/deps.py` — `get_rag_engine()` singleton via `lru_cache`; engine constructed once at startup
- `data/chroma/.gitkeep`, `data/documents/.gitkeep` — folder structure tracked in git, contents gitignored

### ♻️ Changed

- `GET /api/health` — `rag_ready` now reflects real ChromaDB collection state
- `POST /api/chat` — replaced mock token stream with real RAG pipeline; added `session_id` to `ChatRequest`
- `DELETE /api/chat/history` — history now managed by `RAGEngine`, not a module-level list
- `core/config.py` — added `project_root`, `chroma_collection_name`; `chroma_persist_dir` now absolute
- `.gitignore` — `data/chroma/*` and `data/documents/*` ignore contents but keep folders

### 🧪 Tested

- 22 passing tests (unit + integration)
- `tests/unit/test_schemas.py` — `ChatRequest`, `HealthResponse`, `StatusResponse`
- `tests/unit/test_prompts.py` — prompt builder: context injection, history preservation, fallback
- `tests/integration/test_health.py` — health endpoint with mocked engine readiness
- `tests/integration/test_chat.py` — SSE format, token streaming, session routing, history clearing

---

## [0.2.0] — 2026-03-17 — "First Contact"

The API is alive. Real endpoints, real structure, real streaming — mock data for now,
but the frontend can talk to it. A hollow signal, but a signal nonetheless.

### 🎉 Added

- `GET /api/health` — liveness check with `rag_ready` flag (false until RAG is wired)
- `POST /api/chat` — SSE streaming endpoint; yields mock tokens word-by-word, ends with `[DONE]`
- `DELETE /api/chat/history` — clears in-memory conversation history
- `core/config.py` — pydantic-settings `Settings` loading from `.env`
- `core/logging.py` — structured logging configured at startup
- `models/schemas.py` — `ChatRequest`, `StatusResponse`, `HealthResponse` Pydantic v2 models
- `api/deps.py` — dependency injection foundation (ready for RAG engine)
- `api/middleware.py` — CORS registration from `settings.cors_origins`
- `requests/api.http` — HTTP client file for manual endpoint testing

### 🗑️ Removed

- Placeholder hello-world routes (`GET /`, `GET /hello/{name}`)
- `test_main.http` — replaced by `requests/api.http`

### 📝 Docs

- `ARCHITECTURE.md` — added Implementation Backlog with full Phase 1 checklist (12 items to wire up real RAG)

---

## [0.1.1] — 2026-03-17 — "Calibration"

Fine-tuning the instruments before the real signal arrives.
Skills and tooling aligned for Python — no more frontend leftovers.

### 🔧 Fixed

- git-workflow skill: pre-push checklist now uses `uv`/Python commands (was bun/frontend)
- git-workflow skill: commit examples updated to BE context; rule added for `release` skill on PRs to main
- release skill: version location corrected to `pyproject.toml` (was `package.json`)
- release skill: CHANGELOG example replaced with Python/FastAPI/RAG content (was SvelteKit)
- release skill: `allowed-tools` corrected to `Bash(uv:*)` (was `Bash(bun:*)`)

---

## [0.1.0] — 2026-03-17 — "Dark Matter"

The invisible backbone. You can't see it yet, but it holds everything together.
Project scaffold with all the plumbing — ready for the RAG pipeline to light up.

### 🎉 Added
- FastAPI project structure with uv package management
- Claude Code configuration — CLAUDE.md, 6 skills, security rules
- Docker multi-stage build with uv (copying binary from official image)
- API contract defined: POST /api/chat (SSE), DELETE /api/chat/history, GET /api/health
- ARCHITECTURE.md with RAG pipeline design and internal architecture diagrams
- pytest + httpx + ruff + mypy dev tooling
- pyproject.toml with all dependencies (FastAPI, Anthropic SDK, LlamaIndex, ChromaDB)
