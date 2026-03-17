# Stage 1: Install dependencies
FROM python:3.13-slim AS base
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

FROM base AS deps
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Stage 2: Production
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
