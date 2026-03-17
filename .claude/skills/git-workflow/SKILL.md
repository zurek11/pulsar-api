---
name: git-workflow
description: Git operations including branching, emoji commits, and PR creation. Use when committing changes, creating branches, pushing, or opening pull requests.
allowed-tools: Read, Grep, Bash(git:*), Bash(gh:*)
---

# Git Workflow

Same conventions as pulsar-chat — see that repo's git-workflow skill for full details.

## Pre-Push Checklist (Python-specific)

```bash
uv run pytest              # All tests pass
uv run ruff check .        # No lint errors
uv run ruff format --check . # Formatting correct
uv run mypy .              # Type checking passes
```

## Emoji Commit Messages

| Emoji | Type | Example |
|-------|------|---------|
| 🎉 | feat | `🎉 feat: add RAG retrieval with semantic search` |
| 🐛 | fix | `🐛 fix: handle empty vector store gracefully` |
| ♻️ | refactor | `♻️ refactor: extract prompt building into module` |
| 🧪 | test | `🧪 test: add integration tests for SSE streaming` |
| 📝 | docs | `📝 docs: document RAG pipeline in ARCHITECTURE.md` |
| 🔧 | chore | `🔧 chore: bump anthropic SDK to latest` |
| 🐳 | docker | `🐳 docker: add health check endpoint to container` |
| 🚀 | release | `🚀 release: v0.2.0 — RAG comes alive` |

## Rules
1. Never commit directly to `main` — always feature branches + PR
2. Run full pre-push checklist before every push
3. Always create PR with `--reviewer zurek11`
4. Adam can tag `@claude` in PR reviews for automatic fixes
