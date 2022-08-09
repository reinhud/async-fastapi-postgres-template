"""Pydantic schmata used by 'children' ressources."""
import datetime as dt
from typing import Optional

from app.models.base import BaseSchema


class ChildOptionalSchema(BaseSchema):
    """Used to query 'children' table against.
    
    All optional allows to query for every attricbute optionally.
    """
    id: Optional[int] 
    name: Optional[str] 
    birthdate: Optional[dt.date]
    height: Optional[float]
    hobby: Optional[str]
    updated_at: Optional[dt.datetime]
