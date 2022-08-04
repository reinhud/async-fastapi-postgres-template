"""Connection to the Postgres database."""
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_app_settings


def get_async_engine() -> AsyncEngine:
    """Return async database engine."""
    async_engine: AsyncEngine = create_async_engine(
        get_app_settings().database_url,
        echo=True,  # see sql querries executed
        future=True,
    )

    return async_engine


