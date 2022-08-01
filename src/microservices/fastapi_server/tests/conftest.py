import datetime as dt
from typing import Any, Generator
from fastapi import FastAPI
from httpx import AsyncClient

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy_utils import database_exists, create_database
from asgi_lifespan import LifespanManager
from loguru import logger

from app.db.db_session import AsyncSessionLocal, async_engine
from app.models.domain.user import UserCreate


pytest_plugins = ('pytest-asyncio',)

@pytest.fixture
def init_db():
    if not database_exists(async_engine.url):
        logger.warning("Database not found")
        try:
            create_database(async_engine.url)
            logger.info("Database created")
        except:
            logger.error("Couldnt create new database")

@pytest.fixture
def app() -> Generator[FastAPI, Any, None]:
    from app.fastapi_server import get_app
    yield get_app()

@pytest.fixture
def engine(app: FastAPI) -> AsyncEngine:
    return  async_engine

@pytest.fixture
async def async_session() -> Generator:
    async_session = AsyncSession(async_engine, autoflush=False, autocommit=False)
    try:
        return async_session
    finally:
        await async_session.close()

@pytest.fixture
async def async_test_client(app: FastAPI, async_session:AsyncSession) -> Generator:
    from app.api.dependencies.database import get_database
    
    # this needs to be defined inside this fixture
    # this is generate that yields session retrieved from `session` fixture
    
    def get_test_database(): 
        yield async_session
    
    app.dependency_overrides[get_database] = get_test_database
        
    async with AsyncClient(
             app=app, base_url="http://test", 
             ) as ac:
        yield ac


@pytest.fixture
async def user1():
    new_user = UserCreate(
        name="User 1",
        birthdate=dt.date(2000, 1, 1),
        wealth=1
    )
    return new_user