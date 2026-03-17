---
name: git-workflow
description: 'REQUIRED for ALL PRs, pushes, and commits. Invoke this skill before running any gh pr create or git push command.'
allowed-tools: Read, Grep, Bash(git:*), Bash(gh:*)
---

# Git Workflow

## When to Use

- Committing any changes
- Creating feature branches
- Pushing and opening PRs
- Addressing PR review feedback

## Branch Naming

```
feat/[short-description]     # New feature
fix/[short-description]      # Bug fix
refactor/[short-description] # Code refactoring
test/[short-description]     # Adding tests
docs/[short-description]     # Documentation
chore/[short-description]    # Maintenance
docker/[short-description]   # Container changes
```

## Emoji Commit Messages

Every commit MUST start with an emoji. Keep messages fun but informative.

| Emoji | Type     | Example                                                      |
| ----- | -------- | ------------------------------------------------------------ |
| 🎉    | feat     | `🎉 feat: add RAG retrieval endpoint with streaming`         |
| 🐛    | fix      | `🐛 fix: handle empty vector store gracefully`               |
| ♻️    | refactor | `♻️ refactor: extract prompt building into module`           |
| 🧪    | test     | `🧪 test: add integration tests for SSE streaming`           |
| 📝    | docs     | `📝 docs: document RAG pipeline in ARCHITECTURE.md`          |
| 🔧    | chore    | `🔧 chore: bump anthropic SDK, update uv.lock`               |
| 💄    | style    | `💄 style: consistent error response format across routes`   |
| 🐳    | docker   | `🐳 docker: slim down image with multi-stage build`          |
| 🚀    | release  | `🚀 release: v0.2.0 — RAG comes alive`                       |
| 🗑️    | remove   | `🗑️ chore: remove unused utility functions`                  |
| 🔒    | security | `🔒 fix: rotate exposed API key, update env handling`        |
| ⚡    | perf     | `⚡ perf: cache embeddings to skip redundant re-computation` |

### Tone Guide

- Be specific about WHAT changed, not just WHERE
- A little personality is encouraged: "🐛 fix: teach the retriever to handle empty results" > "🐛 fix: fix retriever bug"
- Keep under 72 chars

## Full PR Workflow

### 1. Create branch

```bash
git checkout main
git pull origin main
uv sync --extra dev
git checkout -b feat/rag-pipeline
```

### 2. Implement + test

Write code and tests together. No code without tests.

### 3. Pre-push checklist (ALL must pass)

```bash
uv run pytest              # All tests pass
uv run ruff check .        # No lint errors
uv run ruff format --check . # Formatting correct
uv run mypy .              # Type checking passes
```

### 4. Bump version + changelog

Use the `release` skill. Always bump BEFORE committing.

### 5. Commit and push

```bash
git add pyproject.toml CHANGELOG.md <changed files>
git commit -m "🎉 feat: add RAG retrieval with semantic search"
git push -u origin feat/rag-pipeline
```

### 6. Create PR

PR title and body come from the changelog entry — use the `release` skill.

```bash
gh pr create \
  --title "🚀 Release v0.2.0 — RAG comes alive" \
  --base main \
  --body "$(cat <<'EOF'
<changelog entry for this version>
EOF
)" \
  --reviewer zurek11
```

### 7. After review — two paths

**Path A: @claude directly on GitHub**
Adam leaves a review comment and tags `@claude` in the PR.
Claude GitHub App addresses feedback automatically — commits a fix directly to the PR branch.

**Path B: Via Claude Code locally**

```bash
# Read review feedback
gh pr view 3 --comments

# Fix what's needed, commit + push
git commit -m "🐛 fix: address PR feedback — [specific change]"
git push
```

Both approaches update the PR automatically. Adam re-reviews and merges.

## Rules

1. Never commit directly to `main` — always use feature branches + PR
2. Keep commits atomic — one logical change per commit
3. Public repo: double-check no secrets in diff before push (`git diff --cached | grep -iE "(sk-ant|api.key|token|secret|password)"`)
4. Run full pre-push checklist before every push
5. No `print()` in production code — use `logging` (configured in `core/logging.py`)
6. Always create PR with `--reviewer zurek11`
7. PRs targeting `main` require the `release` skill — invoke it before `gh pr create`
