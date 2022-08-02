import os
import warnings
from glob import glob
from typing import Generator

import alembic
import pytest
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.api.dependencies.database import get_database
from app.core.config import get_app_settings
from app.fastapi_server import app


settings = get_app_settings()


# make "trio" warnings go away :)
@pytest.fixture
def anyio_backend():
    return 'asyncio'


# Allow fixtures that are in \tests\fixtures folder to be included in conftest
# Source: https://gist.github.com/peterhurford/09f7dcda0ab04b95c026c60fa49c2a68
def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")

pytest_plugins = [
    refactor(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture
]


# database setup
@pytest.fixture(scope="session")
def apply_migrations() -> Generator:
    """Apply migrations at beginning and end of testing session."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    # new revision, get freshest changes in db models
    alembic.command.revision(
        message="Revision before test",
        autogenerate=True,
        )
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# fastapi setup
@pytest.fixture
async def async_test_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


# sqlalchemy setup
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
    async_engine = create_async_engine(
        settings.database_url, 
        poolclass=NullPool
        )
    async with async_engine.connect() as conn:

        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
            class_=AsyncSession,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction:
                conn.sync_connection.begin_nested()

        def test_get_database() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError as e:
                pass

        app.dependency_overrides[get_database] = test_get_database

        yield async_session
        await async_session.close()
        await conn.rollback()