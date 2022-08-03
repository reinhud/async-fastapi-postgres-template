"""Abstract CRUD Repo definitions."""
from abc import ABC
from typing import List

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app._utils._types import CREATE_SCHEMA, READ_MULTIPLE_SCHEMA, SQLA_MODEL
from app.db.models.base import BaseSaModel
from app.models.base import BaseSchema


class SQLAlchemyRepository(ABC):
    """Abstract SQLAlchemy repo defining basic database operations.
    
    Basic CRUD methods used by domain models to interact with the
    database are defined here.
    """
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    # models and schemas object instanziation and validation
    sqla_model: SQLA_MODEL

    create_Schema: CREATE_SCHEMA
    read_multiple_schema: READ_MULTIPLE_SCHEMA

    ## ===== Basic Crud Operations ===== ##
    async def create(
        self, 
        obj_new: create_Schema
        ) -> sqla_model | None:
        """Commit new object to the database."""
        try:
            db_obj_new = self.sqla_model(**obj_new.dict())
            self.db.add(db_obj_new)
            await self.db.commit()
            await self.db.refresh(db_obj_new)
            
            return db_obj_new

        except Exception as e:
            await self.db.rollback()
            logger.exception("Error while uploading new object to database")
            logger.exception(e)

            return None


    async def read_by_id(
        self,
        id: int,
    ) -> sqla_model | None:
        """Get object by id or return None."""
        res = await self.db.get(self.sqla_model, id)  # returns none if no entity found
        
        return res


    async def read_multiple(
        self,
        query_schema: READ_MULTIPLE_SCHEMA,
    ) -> List[sqla_model] | None:
        """Get list of all objects that match with query_schema.
        
        If values in query schema are not provided, they will default to None and
        will not be searched for. To search for None values specifically provide
        desired value set to None.
        """
        filters: dict = query_schema.dict(exclude_none=True)
        stmt = select(self.sqla_model).filter_by(**filters).order_by(self.sqla_model.id)
        stream = await self.db.stream(stmt)
        async for row in stream:

            yield row


    async def delete(
        self,
        id: int,
    ) -> sqla_model | None:
        """Delete object from db by id or None if object not found in db"""
        res = await self.db.get(self.sqla_model, id)
        if res:
            await self.db.delete(res)
            await self.db.commit()
        else:
            logger.error(f"Object with id = {id} not found in query")

        return res