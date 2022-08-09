"""Testing parent endpoints.

More like unit tests, we're mocking the actual database calls here.

TODO:
    1. Implement method to test 'read_multiple' asserting streaming results
"""
from fastapi import status
from fastapi.encoders import jsonable_encoder
import pytest

from app.db.repositories.base import SQLAlchemyRepository
from app.models.utility_schemas.parents import ParentOptionalSchema


@pytest.mark.anyio
class Test_Parents():
    """Test class for parent endpoints."""
    async def test_create_parent_OK(
        self,
        async_test_client,
        Parent1_Correct,
        monkeypatch
    ):
        Parent1_Create = Parent1_Correct["create"]
        Parent1_InDB = Parent1_Correct["in_db"]

        # mock the create method that would invoke actual db calls
        async def mock_post(self, obj_new):
            return Parent1_InDB         
        monkeypatch.setattr(SQLAlchemyRepository, "create", mock_post)
        
        res = await async_test_client.post(
            "/api/parents/post",
            json=Parent1_Create
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == Parent1_InDB
        
    
    async def test_read_parent_by_id_OK(
        self,
        async_test_client,
        Parent1_Correct,
        monkeypatch
    ):  
        Parent1_InDB = Parent1_Correct["in_db"]
        params = {"id": 1}

        async def mock_read_by_id(self, id):
            return  Parent1_InDB
        monkeypatch.setattr(SQLAlchemyRepository, "read_by_id", mock_read_by_id)

        res = await async_test_client.get(
            "/api/parents/get_by_id",
            params=params
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == Parent1_InDB


    async def test_read_multiple_parents_OK(
        self,
        async_test_client,
        Parents_List_Correct,
        monkeypatch
    ):  
        query_schema = jsonable_encoder(
            ParentOptionalSchema(
                height=1.90
            )
        )
        Parents_Output = [Parents_dict["in_db"] for Parents_dict in Parents_List_Correct]

        async def mock_read_optional(self, query_schema):
            return Parents_Output
        monkeypatch.setattr(SQLAlchemyRepository, "read_optional", mock_read_optional)

        res = await async_test_client.post(
            "/api/parents/get_optional",
            json=query_schema
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == Parents_Output


    async def test_delete_parent_OK(
        self,
        async_test_client,
        Parent1_Correct,
        monkeypatch
    ):  
        Parent1_InDB = Parent1_Correct["in_db"]
        params = {"id": 1}

        async def mock_delete(self, id):
            return Parent1_InDB
        monkeypatch.setattr(SQLAlchemyRepository, "delete", mock_delete)

        res = await async_test_client.delete(
            "/api/parents/delete",
            params=params
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == Parent1_InDB