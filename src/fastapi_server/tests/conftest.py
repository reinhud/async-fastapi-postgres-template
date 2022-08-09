"""Test Setup.

These fixtures will run before tests are involked with pytest.
"""
from glob import glob
import os
from typing import Generator
import warnings

import alembic
from alembic.config import Config
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from loguru import logger
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy_utils import create_database

from app.api.dependencies.database import get_async_session
from app.core.config import get_app_settings
from app.db.models.base import Base
from app.fastapi_server import app
from app.db.db_session import get_async_engine


settings = get_app_settings()


## ===== Pytest and Backend Setup ===== ##
# =========================================================================== #
# make "trio" warnings go away :)
@pytest.fixture
def anyio_backend():
    return 'asyncio'


# allow fixtures that are in \tests\fixtures folder to be included in conftest
def refactor(string: str) -> str:

    return string.replace("/", ".").replace("\\", ".").replace(".py", "")

pytest_plugins = [
    refactor(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture
]



## ===== Database Setup ===== ##
# =========================================================================== #
@pytest.fixture(scope="session")
async def apply_migrations() -> Generator:
    """Apply migrations at beginning and end of testing session."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"     # tells alembics .env to use test database in migrations
    config = Config("alembic.ini")

    async_engine = get_async_engine()

    TEST_DATABASE = f"{async_engine.url}_test"
  
    async with async_engine.connect() as async_conn:

        await async_conn.run_sync(create_database(TEST_DATABASE))
        # use sqlalchemy ddl for initial table setup
        await async_conn.run_sync(Base.metadata.create_all)
        # automatically revert 'head' to most recennt remaining migration
        await alembic.command.stamp(config, "head")
        # new revision, get freshest changes in db models
        await alembic.command.revision(
            config,
            message="Revision before test",
            autogenerate=True,
            )
        # apply migrations
        await alembic.command.upgrade(config, "head")

        yield

        await alembic.command.downgrade(config, "base")
        await async_conn.run_sync(Base.metadata.drop_all)



## ===== SQLAlchemy Setup ===== ##
# =========================================================================== #
@pytest.fixture
async def session():
    """SqlAlchemy testing suite.

    Using ORM while rolling back changes after commit to have independant test cases.
    
    Implementation of "Joining a Session into an External Transaction (such as for test suite)"
    recipe from sqlalchemy docs : 
    https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    
    Inspiration also found on: 
    https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    """
    async_test_engine = get_async_engine()
    async with async_test_engine.connect() as conn:

        await conn.begin()
        await conn.begin_nested()
        
        async_session = AsyncSession(
            conn,
            expire_on_commit=False
            )

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()

        yield async_session

        await async_session.close()
        await conn.rollback()



## ===== FastAPI Setup ===== ##
# =========================================================================== #
@pytest.fixture()
async def test_app(session) -> FastAPI:
    """Injecting test database as dependancy in app for tests."""

    async def test_get_database() -> Generator:
        yield session
                
    app.dependency_overrides[get_async_session] = test_get_database

    return app
    

@pytest.fixture
async def async_test_client(test_app: FastAPI) -> FastAPI:    
    """Test client that will be used to make requests against our endpoints."""
    async with LifespanManager(test_app):
        async with AsyncClient(
            app=test_app, 
            base_url="http://testserver"
        ) as ac:
            try:

                yield ac

            except SQLAlchemyError as e:
                logger.error("Error while yielding test client")