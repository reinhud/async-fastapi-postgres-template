
"""Endpoints for user model."""
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.api.dependencies.repository import get_repository
from app.db.repositories.user import UserRepository
from app.models.domain.user import UserCreate, UserInDB
from app.models.utility_schemas.user import UserQueryOptionalSchema


router = APIRouter()


# Basic User Endpoints
# =========================================================================== #
@router.post("/post", response_model=UserInDB, name="user: create-user", status_code=status.HTTP_201_CREATED)
async def post_user(
    user_new: UserCreate,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserInDB:
    user_created = await user_repo.create(obj_new=user_new)

    return user_created

@router.get("/get_by_id", response_model=UserInDB | None, name="user: read-one-user")
async def get_one_user(
    id: int,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserInDB | None:
     user_db = await user_repo.read_by_id(id=id)
     if not user_db:
        logger.warning(f"No user with id = {id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id = {id}.")

     return user_db

@router.post("/get_optional", response_model=List[UserInDB] | None, name="user: read-optional-users")
async def get_multiple_users(
    query_schema: UserQueryOptionalSchema,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> List[UserInDB] | None:
    users_db = await user_repo.read_multiple(query_schema=query_schema)
    if not users_db:
        logger.warning(f"No users found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users matching query = {query_schema}.")

    return users_db

@router.delete("/delete", response_model=UserInDB, name="user: delete-user")
async def delete_user(
    id: int,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserInDB:
    user_deleted = await user_repo.delete(id=id)
    if not user_deleted:
        logger.warning(f"No user with id = {id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to delete User with id = {id}, User not found")

    return user_deleted

