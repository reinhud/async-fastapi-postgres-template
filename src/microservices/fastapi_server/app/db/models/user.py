from sqlalchemy import Column, MetaData, String, Numeric, DateTime, Date
from sqlalchemy.sql import func
from app.db.models.base import Base, BaseSaModel

metadata_user = MetaData()

class User(Base, BaseSaModel):

    __metadata__ = metadata_user

    # automatic id
    name = Column(String)
    birthdate = Column(Date)
    wealth = Column(Numeric)
    updated_at = Column(DateTime, server_default=func.now())
    

    