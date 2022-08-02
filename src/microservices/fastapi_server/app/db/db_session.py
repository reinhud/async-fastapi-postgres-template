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
    bind=async_engine, 
    class_=AsyncSession, 
    autoflush=False,
    expire_on_commit=False,   # document this
)

        
        