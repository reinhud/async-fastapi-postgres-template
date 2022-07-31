import datetime as dt
from typing import Optional

from app.models.base import BaseSchema


class UserQueryOptionalSchema(BaseSchema):
    id: Optional[int] 
    name: Optional[str] 
    birthdate: Optional[dt.date]
    wealth: Optional[float]
    updated_at: Optional[dt.datetime]