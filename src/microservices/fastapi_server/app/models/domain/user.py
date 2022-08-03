"""Pydantic domain models for User"""
import datetime as dt
from typing import Optional

from app.models.base import BaseSchema, IDSchemaMixin


class UserBase(BaseSchema):
    name: str
    birthdate: Optional[dt.date]
    height: Optional[float]

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    id: int

class UserInDB(UserBase, IDSchemaMixin):
    """Schema for User in database."""
    updated_at: dt.datetime