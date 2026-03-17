# Changelog

All notable changes to Pulsar API — the RAG-powered backend for the Pulsar learning project.

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
