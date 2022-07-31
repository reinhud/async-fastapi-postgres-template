from os import environ
"""from typing import Any, Generator
from fastapi import FastAPI
from psycopg2 import DatabaseError
from httpx import AsyncClient

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import database_exists

from app.db.db_session import async_engine, AsyncSessionLocal
from app.db.models.base import Base
from app.api.dependencies.database import get_database
"""

environ["app_env"] = "test"
'''


@pytest.fixture(scope="session")
async def init_test_db() -> None:

    if not database_exists(async_engine.url):
        raise DatabaseError("Test database doesnt exist, pls handle it manually")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="function")
def get_test_database() -> Generator[AsyncSession, Any, None]:
    db = AsyncSessionLocal
    db.begin()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope="function")
def app(
    get_test_database: AsyncSessionLocal,
) -> Generator[FastAPI, Any, None]:

    from app.fastapi_server import get_app

    _app = get_app()

    _app.dependency_overrides[get_database] = lambda: get_test_database

    yield _app

@pytest.fixture(scope="function")
async def test_client(
    app: FastAPI,
) -> Generator[AsyncClient, Any, None]:
    """Override get_database dependancy with get_test_database.
    
    This is so each test session transaction is rolled back after commits.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac'''