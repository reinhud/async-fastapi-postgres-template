"""Repository dependancies for FastApi app.

TODO:
    1. do funcs need to be async?
"""
from typing import Callable, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app._utils._types import SQLA_REPO_TYPE
from app.api.dependencies.database import get_async_session


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