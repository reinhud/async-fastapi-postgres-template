from typing import Any

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin, declarative_base
from sqlalchemy.ext.declarative import declared_attr


Base = declarative_base()

@declarative_mixin
class BaseSaModel:
    # autoinc pk key
    id = Column(Integer, primary_key=True, autoincrement=True)
    __name__: str

    # if not declared generate tablename automatically based on class name 
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # refresh server defaults with asyncio 
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#synopsis-orm
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}
