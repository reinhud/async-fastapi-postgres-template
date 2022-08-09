"""Sqlalchemy model for 'parent' table."""
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base, BaseDBModel
from app.db.models.metadata import metadata_family


class Child(Base, BaseDBModel):
    """ Database model representing 'parent' table in db.
    
    'id' and 'tablename' are created automatically by 'BaseDBModel'.
    """
    __metadata__ = metadata_family

    name = Column(String)
    birthdate = Column(Date)
    height = Column(Numeric)
    hobby= Column(String)
    parent_id = Column(Integer, ForeignKey("parent.id"))
    parent = relationship("Parent", back_populates="children")