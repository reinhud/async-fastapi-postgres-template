"""Domain Repository for 'parent' entity.

All logic related to the parent entity is defined and grouped here.
"""
from typing import List

from sqlalchemy import select

from app.db.models.parents import Parent as ParentModel
from app.db.models.children import Child as ChildModel
from app.db.repositories.base import SQLAlchemyRepository
from app.models.domain.parents import ParentCreate
from app.models.utility_schemas.parents import ParentOptionalSchema


class ParentRepository(SQLAlchemyRepository):
    """Handle all logic related to Parent entity.
    
    Inheritence from 'SQLAlchemyRepository' allows for 
    crud functionality, only schemata and models used have to be defined.
    """
    sqla_model = ParentModel

    create_schema = ParentCreate
    read_optional_schema = ParentOptionalSchema


    # Testing relationship patterns are working
    async def get_parent_children(
        self,
        id: int,
    ) -> List[sqla_model] | None:
        """Get all children belonging to a certain parent."""
        stmt = select(ChildModel).join(self.sqla_model, ChildModel.parent_id == self.sqla_model.id)

        res = await self.db.execute(stmt)
        res = res.scalars().all()

        return res
