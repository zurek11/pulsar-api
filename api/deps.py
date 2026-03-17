"""FastAPI dependency providers for pulsar-api."""

from fastapi import Depends

from core.config import Settings, get_settings

# Re-export so routes import from a single place
__all__ = ["get_settings", "provide_settings"]


def provide_settings(settings: Settings = Depends(get_settings)) -> Settings:  # noqa: B008
    """Inject application settings into route handlers."""
    return settings
