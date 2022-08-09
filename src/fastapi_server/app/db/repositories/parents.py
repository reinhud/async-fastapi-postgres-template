"""Domain Repository for 'parent' entity.

All logic related to the parent entity is defined and grouped here.
"""
from app.db.models.parents import Parent as ParentModel
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
    read_multiple_schema = ParentOptionalSchema
