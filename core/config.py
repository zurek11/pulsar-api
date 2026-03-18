"""Application settings loaded from environment / .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for Pulsar API.

    Values are read from environment variables or a `.env` file at project root.
    Never hard-code secrets — add them to `.env` (gitignored) and reference here.
    """

    # Resolved from this file's location — always points to the repo root.
    project_root: Path = Path(__file__).parent.parent

    anthropic_api_key: str = "not-set"
    model_name: str = "claude-sonnet-4-6"
    chroma_persist_dir: str = str(Path(__file__).parent.parent / "data" / "chroma")
    chroma_collection_name: str = "pulsar_docs"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 5
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
