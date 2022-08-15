"""Endpoints for 'parent' ressource."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.api.dependencies.repository import get_repository
from app.db.repositories.parents import ParentRepository
from app.models.domain.parents import ParentCreate, ParentInDB
from app.models.domain.children import ChildInDB
from app.models.utility_schemas.parents import ParentOptionalSchema


router = APIRouter()


# Basic Parent Endpoints
# =========================================================================== #
@router.post("/post", response_model=ParentInDB, name="parents: create-parent", status_code=status.HTTP_201_CREATED)
async def post_parent(
    parent_new: ParentCreate,
    parent_repo: ParentRepository = Depends(get_repository(ParentRepository)),
) -> ParentInDB:
    parent_created = await parent_repo.create(obj_new=parent_new)

    return parent_created

@router.get("/get_by_id", response_model=ParentInDB | None, name="parents: read-one-parent")
async def get_one_parent(
    id: int,
    parent_repo: ParentRepository = Depends(get_repository(ParentRepository)),
) -> ParentInDB | None:
     parent_db = await parent_repo.read_by_id(id=id)
     if not parent_db:
        logger.warning(f"No parent with id = {id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No parent with id = {id}.")

     return parent_db

@router.post("/get_optional", name="parents: read-optional-parents")    #, response_model=List[ParentInDB] | None
async def get_optional_parents(
    query_schema: ParentOptionalSchema,
    parent_repo: ParentRepository = Depends(get_repository(ParentRepository)),
) -> List[ParentInDB] | None:
    parents_db = await parent_repo.read_optional(query_schema=query_schema)
    if not parents_db:
        logger.warning(f"No Pprents found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No parents matching query: {query_schema.dict(exclude_none=True)}.")

    return parents_db

@router.delete("/delete", response_model=ParentInDB, name="parents: delete-parent")
async def delete_parent(
    id: int,
    parent_repo: ParentRepository = Depends(get_repository(ParentRepository)),
) -> ParentInDB:
    parent_deleted = await parent_repo.delete(id=id)
    if not parent_deleted:
        logger.warning(f"No parent with id = {id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to delete parent with id = {id}, Parent not found")

    return parent_deleted



# Basic relationship pattern endpoint
# =========================================================================== #
@router.get("/get_children", name="parents: get-all-children-for-parent") #response_model=List[ChildInDB]
async def get_parent_children(
    id: int,
    parent_repo: ParentRepository = Depends(get_repository(ParentRepository)),
) -> List[ChildInDB] | None:
    children = await parent_repo.get_parent_children_by_id(id=id)
    if children is None:
        logger.info(f"Parent with id: {id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Parent with id: {id} not found.")
    elif not children:
        logger.info(f"Parent with id: {id} has no children.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No children found for parent with with id: {id}.")
    return children