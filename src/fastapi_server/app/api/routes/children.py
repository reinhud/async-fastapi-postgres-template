"""Endpoints for 'children' ressource."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.api.dependencies.repository import get_repository
from app.db.repositories.children import ChildRepository
from app.models.domain.children import ChildCreate, ChildInDB
from app.models.utility_schemas.children import ChildOptionalSchema


router = APIRouter()


# Basic Parent Endpoints
# =========================================================================== #
@router.post("/post", response_model=ChildInDB, name="Children: create-child", status_code=status.HTTP_201_CREATED)
async def post_child(
    child_new: ChildCreate,
    child_repo: ChildRepository = Depends(get_repository(ChildRepository)),
) -> ChildInDB:
    child_created = await child_repo.create(obj_new=child_new)

    return child_created

@router.get("/get_by_id", response_model=ChildInDB | None, name="children: read-one-child")
async def get_one_child(
    id: int,
    child_repo: ChildRepository = Depends(get_repository(ChildRepository)),
) -> ChildInDB | None:
     child_db = await child_repo.read_by_id(id=id)
     if not child_db:
        logger.warning(f"No child with id = {id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No child with id = {id}.")

     return child_db

@router.post("/get_optional", response_model=List[ChildInDB] | None, name="children: read-optional-children")
async def get_optional_children(
    query_schema: ChildOptionalSchema,
    child_repo: ChildRepository = Depends(get_repository(ChildRepository)),
) -> List[ChildInDB] | None:
    children_db = await child_repo.read_optional(query_schema=query_schema)
    if not children_db:
        logger.warning(f"No children found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No children matching query: {query_schema.dict(exclude_none=True)}.")

    return children_db

@router.delete("/delete", response_model=ChildInDB, name="children: delete-child")
async def delete_child(
    id: int,
    child_repo: ChildRepository = Depends(get_repository(ChildRepository)),
) -> ChildInDB:
    parent_deleted = await child_repo.delete(id=id)
    if not parent_deleted:
        logger.warning(f"No parent with id = {id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to delete child with id = {id}, Parent not found")

    return parent_deleted