---
name: docker
description: Docker and docker-compose patterns for pulsar-api. Use when creating Dockerfiles, docker-compose configs, or troubleshooting container issues.
allowed-tools: Read, Write, Edit, Bash(docker:*), Bash(uv:*)
---

# Docker Patterns

## Dockerfile — Multi-Stage Build with uv

```dockerfile
FROM python:3.13-slim AS base
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

FROM base AS deps
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM base AS production
COPY --from=deps /app/.venv .venv
COPY main.py .
COPY api/ api/
COPY core/ core/
COPY llm/ llm/
COPY models/ models/
COPY rag/ rag/
COPY data/ data/
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Rules
1. Multi-stage builds — keep production image slim
2. Use `python:3.13-slim` as base
3. Copy uv binary from official image for install stage
4. `--frozen --no-dev` for deterministic production installs
5. Never include `.env` in image — pass via `--env-file` at runtime
6. `data/documents/` may need volume mounting for large knowledge bases
