import asyncio
from logging.config import fileConfig
import os
import pathlib
import sys

from alembic import context
from loguru import logger
from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool import NullPool

# allow migrations to import from 'app'
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from app.core.config import get_app_settings
from app.db.models.base import Base
from app.db.models.metadata import metadata_family


settings = get_app_settings()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
#    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # varies between live and test migrations
    DATABASE_URL = f"{settings.database_url}_test" if os.environ.get("TESTING") else settings.database_url

    connectable = context.config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
    if connectable is None:
        connectable = AsyncEngine(
            engine_from_config(
                context.config.get_section(context.config.config_ini_section),
                prefix="sqlalchemy.",
                poolclass=NullPool,
                # future=True
            )
        )
        
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    logger.info("Running migrations offline.")
    run_migrations_offline()
else:
    logger.info("Running migrations online.")
    asyncio.run(run_migrations_online())
