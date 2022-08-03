"""Pydantic schmata used by user ressources."""
import datetime as dt
from typing import Optional

from app.models.base import BaseSchema


class UserQueryOptionalSchema(BaseSchema):
    """Userd to query user table against.
    
    All optional allows to query for every attricbute optionally.
    """
    id: Optional[int] 
    name: Optional[str] 
    birthdate: Optional[dt.date]
    height: Optional[float]
    updated_at: Optional[dt.datetime]