"""Pydantic schmata used by 'children' ressources."""
import datetime as dt
from typing import Optional

from app.models.base import BaseSchema


class ChildOptionalSchema(BaseSchema):
    """Used to query 'children' table against.
    
    All optional allows to query for every attricbute optionally.
    """
    id: Optional[int] = None
    name: Optional[str] = None 
    birthdate: Optional[dt.date] = None
    height: Optional[float] = None
    hobby: Optional[str] = None
    updated_at: Optional[dt.datetime] = None
