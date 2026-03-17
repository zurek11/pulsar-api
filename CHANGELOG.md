# Changelog

All notable changes to Pulsar API — the RAG-powered backend for the Pulsar learning project.

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
