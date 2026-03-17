---
name: release
description: 'REQUIRED when creating a release PR to main or bumping the version. Invoke this skill before touching pyproject.toml version or running gh pr create targeting main.'
allowed-tools: Read, Write, Edit, Bash(uv:*), Bash(git:*), Bash(gh:*)
---

# Release & Versioning

## When to Use

- Bumping version before a PR
- Writing or updating CHANGELOG.md
- Creating a release PR to main

## Semantic Versioning

Version lives in `pyproject.toml` → `version = "X.Y.Z"`

| Bump          | When                                 | Example       |
| ------------- | ------------------------------------ | ------------- |
| **MAJOR** (X) | Breaking API changes, major rewrites | 0.x → 1.0.0   |
| **MINOR** (Y) | New features, backward compatible    | 0.1.0 → 0.2.0 |
| **PATCH** (Z) | Bug fixes, small improvements        | 0.2.0 → 0.2.1 |

During v0.x.x (pre-1.0), treat MINOR as "new features" and PATCH as "fixes/tweaks".

## CHANGELOG.md Format

The changelog should be **fun to read** — not a dry list. Each release gets a nickname and personality.

```markdown
# Changelog

All notable changes to Pulsar API.

## [0.3.0] — 2026-04-01 — "Signal Boost"

The retriever finally grew a brain. Hybrid search lands — BM25 meets
semantic, cross-encoder re-ranks the noise away.

### 🎉 Added

- Hybrid retrieval — BM25 lexical search alongside semantic search
- Cross-encoder re-ranking: top-50 → top-5 with sentence-transformers
- Metadata filtering by source document and date

### 🐛 Fixed

- RAG engine no longer crashes on empty document collection (oops)
- Embedding model now loads lazily — startup time cut by 3s

### ♻️ Changed

- Switched vector store from in-memory ChromaDB to persistent mode
- Retriever now returns source metadata alongside content chunks

---

## [0.2.0] — 2026-03-25 — "First Contact"

The API is alive. Real endpoints, real RAG, real streaming.
Ask it something — it might even answer correctly.

### 🎉 Added

- POST /api/chat with SSE streaming via EventSourceResponse
- DELETE /api/chat/history to reset conversation
- GET /api/health with RAG readiness check
- Phase 1 RAG pipeline: ingest → chunk → embed → ChromaDB → retrieve → stream
- In-memory chat history with session support
- pydantic-settings config loaded from .env

### 🧪 Tested

- Integration tests for all three endpoints
- Unit tests for retriever and prompt builder

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
```

### Tone Guide for Release Notes

- Each version gets a **nickname** — space/astronomy themed preferred but not required
- Open with 1-2 sentences that tell the STORY of this release
- Use emojis in section headers
- Be honest and human: "finally", "oops", "baby steps" are encouraged
- Mention the WHY, not just the WHAT
- Someone should enjoy reading this, not just scanning it

## Release Steps

### 1. Determine version bump

Look at commits since last release:

- Any new feature? → MINOR bump
- Only fixes/chores? → PATCH bump
- Breaking change? → MAJOR bump

### 2. Update pyproject.toml

```bash
# Read current version
grep '^version' pyproject.toml

# Edit the version field manually
# e.g., 0.1.0 → 0.2.0
```

### 3. Update CHANGELOG.md

Add new section at TOP of changelog, below the header.
Follow the format above. Include a release nickname.

### 4. Commit the release

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "🚀 release: v0.2.0 — First Contact"
```

### 5. Create PR

PR title format: `🚀 Release vX.Y.Z — Nickname`
PR body: copy the changelog section for this version exactly.
Always add `--reviewer zurek11`.

### 6. After merge (Adam does this)

```bash
git tag v0.2.0
git push origin v0.2.0
```

## Rules

1. Version bump happens BEFORE the final commit, not after
2. CHANGELOG.md is always updated alongside version bump
3. Every release gets a nickname
4. Release notes should be enjoyable to read
5. Never skip the changelog — even for patch releases
