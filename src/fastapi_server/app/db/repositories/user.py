"""Domain Repository for user entity.

All logic related to the user entity is defined and grouped here.
"""
from app.db.models.user import User as UserModel
from app.db.repositories.base import SQLAlchemyRepository
from app.models.domain.user import UserCreate
from app.models.utility_schemas.user import UserQueryOptionalSchema


class UserRepository(SQLAlchemyRepository):
    """Handle all logic related to user entity.
    
    Inheritence from 'SQLAlchemyRepository' allows for 
    crud functionality, only schemata and models used have to be defined.
    """
    sqla_model = UserModel

    create_schema = UserCreate
    read_multiple_schema = UserQueryOptionalSchema

    

