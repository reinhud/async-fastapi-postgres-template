"""Pydantic domain models for 'children' ressource."""
import datetime as dt
from typing import Optional

from app.models.base import BaseSchema, IDSchemaMixin


class ChildBase(BaseSchema):
    name: str
    birthdate: Optional[dt.date]
    height: Optional[float]
    hobby: Optional[str]
    parent_id: int

class ChildCreate(ChildBase):
    pass

class ChildUpdate(ChildBase):
    id: int

class ChildInDB(ChildBase, IDSchemaMixin):
    """Schema for 'child' in database."""
    updated_at: dt.datetime