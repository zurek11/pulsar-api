# Security — Public Repository

This is a PUBLIC GitHub repository. Every file committed is visible to everyone.

## Absolute Rules
- NEVER include API keys, tokens, passwords, or secrets in any file
- NEVER hardcode the Anthropic API key — always load from environment
- NEVER commit `.env` files — use `.env.example` with placeholder values
- All sensitive configuration via `pydantic-settings` loading from `.env`

## If You Need a Secret
1. Add it to `.env` (gitignored)
2. Add a placeholder to `.env.example`
3. Load it in `src/core/config.py` via pydantic-settings `BaseSettings`

## Before Every Push
```bash
git diff --cached | grep -iE "(sk-ant|api.key|token|secret|password)" || echo "Clean"
```
