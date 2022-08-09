"""Domain Repository for 'child' entity.

All logic related to the child entity is defined and grouped here.
"""
from app.db.models.children import Child as ChildModel
from app.db.repositories.base import SQLAlchemyRepository
from app.models.domain.children import ChildCreate
from app.models.utility_schemas.children import ChildOptionalSchema


class ChildRepository(SQLAlchemyRepository):
    """Handle all logic related to Child entity.
    
    Inheritence from 'SQLAlchemyRepository' allows for 
    crud functionality, only schemata and models used have to be defined.
    """
    sqla_model = ChildModel

    create_schema = ChildCreate
    read_optional_schema = ChildOptionalSchema