"""Application settings loaded from environment / .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pulsar API configuration."""

    anthropic_api_key: str = "not-set"
    model_name: str = "claude-sonnet-4-6"
    chroma_persist_dir: str = "./data/chroma"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 5
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173"

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
