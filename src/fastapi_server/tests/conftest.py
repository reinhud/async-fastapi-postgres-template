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

from app.api.dependencies.database import get_async_session
from app.core.config import get_app_settings
from app.db.models.base import Base
from app.fastapi_server import app


settings = get_app_settings()


## ===== Pytest and Backend Setup ===== ##
# =========================================================================== #
# make "trio" warnings go away :)
@pytest.fixture
def anyio_backend():

    return 'asyncio'

# allow fixtures that are in \tests\fixtures folder to be included in conftest
# source: https://gist.github.com/peterhurford/09f7dcda0ab04b95c026c60fa49c2a68
def refactor(string: str) -> str:

    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [
    refactor(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture
]



## ===== Database Setup ===== ##
# =========================================================================== #
@pytest.fixture(scope="session")
def apply_migrations() -> Generator:
    """Apply migrations at beginning and end of testing session."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    # connect to db via sync engine
    DEFAULT_DB_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db}"
    default_engine = create_engine(DEFAULT_DB_URL, 
    echo=True,
    isolation_level="AUTOCOMMIT"
    )
    # drop testing db if it exists and create a fresh one
    with default_engine.connect() as default_conn:
        # create fresh db for testing
        default_conn.execute(f"DROP DATABASE IF EXISTS {settings.postgres_db}_test")
        default_conn.execute(f"CREATE DATABASE {settings.postgres_db}_test")

        # use sqlalchemy ddl for initial table setup
        Base.metadata.create_all(bind=default_conn)

        # automatically revert 'head' to most recennt remaining migration
        alembic.command.stamp(config, "head")
        # new revision, get freshest changes in db models
        alembic.command.revision(
            config,
            message="Revision before test",
            autogenerate=True,
            )
        alembic.command.upgrade(config, "head")

        yield

        alembic.command.downgrade(config, "base")
        Base.metadata.drop_all(bind=default_conn)



## ===== SQLAlchemy Setup ===== ##
# =========================================================================== #
@pytest.fixture
async def async_test_engine() -> AsyncEngine:
    engine = create_async_engine(
        settings.database_url, 
        echo=True,
        future=True,
    )

    yield engine


@pytest.fixture
async def session(async_test_engine):
    """SqlAlchemy testing suite.

    Using ORM while rolling back changes after commit to have independant test cases.
    
    Implementation of "Joining a Session into an External Transaction (such as for test suite)"
    recipe from sqlalchemy docs : 
    https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    
    Inspiration also found on: 
    https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    """
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

    async def test_get_database() -> Generator:
        yield session
                
    app.dependency_overrides[get_async_session] = test_get_database

    return app
    

@pytest.fixture
async def async_test_client(test_app: FastAPI) -> FastAPI:    
    async with LifespanManager(test_app):
        async with AsyncClient(
            app=test_app, 
            base_url="http://testserver"
        ) as ac:
            try:

                yield ac

            except SQLAlchemyError as e:
                logger.error("Error while yielding test client")