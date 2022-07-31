from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_app_settings
from app.db.models.base import Base


DATABASE_URL = get_app_settings().database_url

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # get logs for sqlalchemy querries
    future=True,
)

AsyncSessionLocal: AsyncSession = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False,   # document this
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        