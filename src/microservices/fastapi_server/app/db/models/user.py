"""Sqlalchemy model for user table."""
from sqlalchemy import Column, Date, MetaData, Numeric, String

from app.db.models.base import Base, BaseSaModel


metadata_user = MetaData()

class User(Base, BaseSaModel):
    """ Database model representing user table in db.
    
    'id' and 'tablename' are created automatically by 'BaseSAModel'.
    """
    __metadata__ = metadata_user

    name = Column(String)
    birthdate = Column(Date)
    height = Column(Numeric)
    

    