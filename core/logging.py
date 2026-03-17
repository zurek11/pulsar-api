"""Structured logging setup for pulsar-api."""

import logging

from core.config import get_settings


def configure_logging() -> None:
    """Configure root logger based on settings."""
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
