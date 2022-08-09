"""Connection to the Postgres database."""
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_app_settings
from app.db.models.base import Base


def get_async_engine() -> AsyncEngine:
    """Return async database engine."""
    try:
        async_engine: AsyncEngine = create_async_engine(
            get_app_settings().database_url,
            future=True,
        )
    except SQLAlchemyError as e:
        logger.warning("Unable to establish db engine, database might not exist yet")
        logger.warning(e)

    return async_engine


async def initialize_database() -> None:
    """Create table in metadata if they don't exist yet.
    
    This uses a sync connection because the 'create_all' doesn't
    feature async yet.
    """
    async_engine = get_async_engine()
    async with async_engine.begin() as async_conn:

        await async_conn.run_sync(Base.metadata.create_all)

        logger.success("Initializing database was successfull.")





