"""Repository dependancies for FastApi app.

TODO:
    1. do funcs need to be async?
"""
from typing import Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_async_session
from app.db.repositories.base import SQLAlchemyRepository


SQLA_REPO_TYPE = TypeVar("SQLA_REPO_TYPE", bound=SQLAlchemyRepository)


# Repo dependency
def get_repository(
    repo_type: Type[SQLA_REPO_TYPE],
    ) -> Callable[[AsyncSession], Type[SQLA_REPO_TYPE]]:
    """Returns specified repository seeded with an async database session."""
    def get_repo(
        db: AsyncSession = Depends(get_async_session),
    ) -> Type[SQLA_REPO_TYPE]:
        return repo_type(db=db)

    return get_repo