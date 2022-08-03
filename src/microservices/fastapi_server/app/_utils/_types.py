"""Types for app"""

"""Custom types for app."""
from typing import TypeVar

from app.db.models.base import Base
from app.db.repositories.base import SQLAlchemyRepository
from app.models.base import BaseSchema


# repos
SQLA_REPO_TYPE = TypeVar("SQLA_REPO_TYPE", bound=SQLAlchemyRepository)

# sqlalchemy models
SQLA_MODEL = TypeVar("SQLA_MODEL", bound=Base)

# pydantic models
CREATE_SCHEMA = TypeVar("CREATE_SCHEMA", bound=BaseSchema)
READ_MULTIPLE_SCHEMA = TypeVar("READ_MULTIPLE_SCHEMA", bound=BaseSchema)