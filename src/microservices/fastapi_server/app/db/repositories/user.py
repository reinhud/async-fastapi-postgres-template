from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.base import SQLAlchemyRepository
from app.db.models.user import User as UserModel
from app.models.domain.user import UserCreate
from app.models.utility_schemas.user import UserQueryOptionalSchema


class UserRepository(SQLAlchemyRepository):
    
    sa_model = UserModel

    create_Schema = UserCreate
    read_optional_schema = UserQueryOptionalSchema

    

