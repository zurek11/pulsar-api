# Changelog

All notable changes to Pulsar API — the RAG-powered backend for the Pulsar learning project.

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
