"""Pydantic domain models for 'parents' ressource."""
import datetime as dt
from typing import Optional

from app.models.base import BaseSchema, IDSchemaMixin


class ParentBase(BaseSchema):
    name: str
    birthdate: Optional[dt.date]
    height: Optional[float]

class ParentCreate(ParentBase):
    pass

class ParentUpdate(ParentBase):
    id: int

class ParentInDB(ParentBase, IDSchemaMixin):
    """Schema for 'parent' in database."""
    updated_at: dt.datetime