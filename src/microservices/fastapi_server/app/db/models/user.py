from sqlalchemy import Column, MetaData, String, Numeric,  Date
from app.db.models.base import Base, BaseSaModel

metadata_user = MetaData()

class User(Base, BaseSaModel):

    __metadata__ = metadata_user

    # automatic id
    name = Column(String)
    birthdate = Column(Date)
    height = Column(Numeric)
    

    