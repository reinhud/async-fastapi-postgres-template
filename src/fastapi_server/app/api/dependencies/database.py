"""Database ependancies for FastApi app.

TODO:
    1. do funcs need to be async?
"""
from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.db_session import get_async_engine


# DB dependency
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session.
    
    All conversations with the database are established via the session
    objects. Also. the sessions act as holding zone for ORM-mapped objects.
    """
    async_session = sessionmaker(
        bind=get_async_engine(), 
        class_=AsyncSession, 
        autoflush=False,
        expire_on_commit=False,   # document this
    )
    async with async_session() as async_sess:
        try:
            
            yield async_sess

        except SQLAlchemyError as e:
            logger.error("Unable to yield session in database dependency")
            logger.error(e)
        