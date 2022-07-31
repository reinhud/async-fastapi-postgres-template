"""Base abstract repo definition.

TODO:
    1. Make exceptions more specific
    2. Type hinting improvements
    3. in case object was not found can still return empty body and make 404 status in response instead of just raising error
"""
from typing import List, Type, Union

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import BaseSaModel
from app.models.base import BaseSchema


class SQLAlchemyRepository():
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    sa_model = BaseSaModel

    create_Schema = BaseSchema
    read_optional_schema = BaseSchema

    async def create(
        self, 
        obj_new: create_Schema
        ) -> sa_model:
        #try:
        db_obj = self.sa_model(**obj_new.dict())
        self.db.add(db_obj)
        await self.db.commit()
        

        return db_obj
        """except Exception as e:
            await self.db.rollback()
            #raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error, you suck at programming") 
            raise e"""

    async def read_by_id(
        self,
        id: int,
    ) -> sa_model:
        res = await self.db.get(self.sa_model, id)  # returns none if no entity found
        if not res:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No {self.sa_model.__tablename__} with id={id} found in corresponding query")
        
        return res

    async def read_optional(
        self,
        query_schema: read_optional_schema,
    ) -> Union[List[sa_model], None]:
        filters: dict = query_schema.dict(exclude_none=True)
        stmt = select(self.sa_model).filter_by(**filters).order_by(self.sa_model.id)
        res = await self.db.execute(stmt)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No {self.sa_model.__tablename__} found in corresponding query with querry params {query_schema.dict()}')
        res = res.scalars().all()   # fetch all rows in list from result object

        return res

    async def delete(
        self,
        id: int,
    ) -> Union[sa_model, None]:
        res = await self.db.get(self.sa_model, id)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No {self.sa_model.__tablename__} with id={id} found in corresponding query")
        try:
            await self.db.delete(res)
            await self.db.commit()

            return res
        except:
            raise Exception