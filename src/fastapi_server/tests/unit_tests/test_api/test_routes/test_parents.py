"""Testing parent endpoints.

More like unit tests, we're mocking the actual database calls here.
"""
from fastapi import status
from fastapi.encoders import jsonable_encoder
import pytest

from app.db.repositories.base import SQLAlchemyRepository
from app.db.repositories.parents import ParentRepository
from app.models.utility_schemas.parents import ParentOptionalSchema


@pytest.mark.anyio
class Test_Parents_Positive():
    """Test class for parent endpoints."""
    # Basic Parent Endpoints
    # ====================================================================== #
    async def test_create_parent_OK(
        self,
        async_test_client,
        Parent3_Create,
        Parent3_InDB_Schema,
        monkeypatch,
    ):
        # mock the create method that would invoke actual db calls
        async def mock_post(self, obj_new):
            return Parent3_InDB_Schema         
        monkeypatch.setattr(SQLAlchemyRepository, "create", mock_post)
        
        res = await async_test_client.post(
            "/api/parents/post",
            json=Parent3_Create
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == Parent3_InDB_Schema
        
    
    async def test_read_parent_by_id_OK(
        self,
        async_test_client,
        Parent3_InDB_Schema,
        monkeypatch,
    ):  
        params = {"id": 3}

        async def mock_read_by_id(self, id):
            return  Parent3_InDB_Schema
        monkeypatch.setattr(SQLAlchemyRepository, "read_by_id", mock_read_by_id)

        res = await async_test_client.get(
            "/api/parents/get_by_id",
            params=params
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == Parent3_InDB_Schema


    async def test_read_multiple_parents_OK(
        self,
        async_test_client,
        Parent1_InDB_Schema,
        Parent2_InDB_Schema,
        monkeypatch,
    ):  
        query_schema = jsonable_encoder(
            ParentOptionalSchema(
                height=1.90
            )
        )
        parents_in_db = [Parent1_InDB_Schema, Parent2_InDB_Schema]

        async def mock_read_optional(self, query_schema):
            return parents_in_db
        monkeypatch.setattr(SQLAlchemyRepository, "read_optional", mock_read_optional)

        res = await async_test_client.post(
            "/api/parents/get_optional",
            json=query_schema
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == parents_in_db


    async def test_delete_parent_OK(
        self,
        async_test_client,
        Parent1_InDB_Schema,
        monkeypatch,
    ):  
        params = {"id": 1}

        async def mock_delete(self, id):
            return Parent1_InDB_Schema
        monkeypatch.setattr(SQLAlchemyRepository, "delete", mock_delete)

        res = await async_test_client.delete(
            "/api/parents/delete",
            params=params
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == Parent1_InDB_Schema


    # Basic relationship pattern endpoint
    # ====================================================================== #
    async def test_get_parent_children_by_id_OK(
        self,
        async_test_client,
        Child1_InDB_Schema,
        Child2_InDB_Schema,
        monkeypatch,
    ):     
        children_of_id_1 = [Child1_InDB_Schema, Child2_InDB_Schema]
        params = {"id": 1}

        async def get_parent_children_by_id(self, id):
            return children_of_id_1
        monkeypatch.setattr(ParentRepository, "get_parent_children_by_id", get_parent_children_by_id)

        res = await async_test_client.get(
            "/api/parents/get_children",
            params=params
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == children_of_id_1



@pytest.mark.anyio
class Test_Parents_Negative():
    """Test class for parent endpoints for negative test cases."""
    # Basic Parent Endpoints
    # ====================================================================== #
    async def test_read_parent_by_id_NOT_FOUND(
        self,
        async_test_client,
        monkeypatch,
    ):  
        params = {"id": 999}

        async def mock_read_by_id(self, id):
            return  None
        monkeypatch.setattr(SQLAlchemyRepository, "read_by_id", mock_read_by_id)

        res = await async_test_client.get(
            "/api/parents/get_by_id",
            params=params
        )

        assert res.status_code == status.HTTP_404_NOT_FOUND
        detail = res.json()
        assert res.json() == {'detail': f'No parent with id = {params["id"]}.'}


    # Basic relationship pattern endpoint
    # ====================================================================== #
    async def test_get_parent_children_by_id_NOT_FOUND(
        self,
        async_test_client,
        monkeypatch,
    ):     
        params = {"id": 999}

        async def mock_get_parent_children_by_id(self, id):
            return None
        monkeypatch.setattr(ParentRepository, "get_parent_children_by_id", mock_get_parent_children_by_id)

        res = await async_test_client.get(
            "/api/parents/get_children",
            params=params
        )

        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res.json() == {'detail': f'Parent with id: {params["id"]} not found.'}

