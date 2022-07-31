
from typing import List, Union
from fastapi import APIRouter, Depends, status

from app.db.repositories.user import UserRepository
from app.api.dependencies.database import get_repository
from app.models.domain.user import UserCreate, UserInDB
from app.models.utility_schemas.user import UserQueryOptionalSchema

# test
from app.db.models.user import User


router = APIRouter(
    prefix="/user",
    tags=["User Endpoints"],
)


# Basic Endpoints
# =========================================================================== #
@router.post("/post", response_model=UserInDB, name="user: create-user", status_code=status.HTTP_201_CREATED)
async def post_user(
    user_new: UserCreate,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserInDB:
    user_created = await user_repo.create(obj_new=user_new)

    return user_created

@router.get("/get_by_id", response_model=Union[UserInDB, None], name="user: read-one-user")
async def get_one_user(
    id: int,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> Union[UserInDB, None]:
     user_db = await user_repo.read_by_id(id=id)

     return user_db

@router.post("/get_optional", response_model=Union[List[UserInDB], None], name="user: read-optional-users")
async def get_optinal_users(
    query_schema: UserQueryOptionalSchema,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> Union[List[UserInDB], None]:
    users_db = await user_repo.read_optional(query_schema=query_schema)

    return users_db

@router.delete("/delete", response_model=UserInDB, name="user: delete-user")
async def delete_user(
    id: int,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserInDB:
    user_deleted = await user_repo.delete(id=id)

    return user_deleted

