"""Testing user endpoints.

More like unit tests, we're mocking the actual database calls here.
"""
from fastapi import status
from fastapi.encoders import jsonable_encoder
import pytest

from app.db.repositories.base import SQLAlchemyRepository
from app.models.utility_schemas.user import UserQueryOptionalSchema


@pytest.mark.anyio
class Test_User():
    """Test class for user endpoints."""
    async def test_create_user_OK(
        self,
        async_test_client,
        User1_Correct,
        monkeypatch
    ):
        User1_Create = User1_Correct["create"]
        User1_InDB = User1_Correct["in_db"]

        # mock the create method that would invoke actual db calls
        async def mock_post(self, obj_new):
            return User1_InDB         
        monkeypatch.setattr(SQLAlchemyRepository, "create", mock_post)
        
        res = await async_test_client.post(
            "/api/user/post",
            json=User1_Create
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == User1_InDB
        
    
    async def test_read_user_by_id_OK(
        self,
        async_test_client,
        User1_Correct,
        monkeypatch
    ):  
        User1_InDB = User1_Correct["in_db"]
        params = {"id": 1}

        async def mock_read_by_id(self, id):
            return  User1_InDB
        monkeypatch.setattr(SQLAlchemyRepository, "read_by_id", mock_read_by_id)

        res = await async_test_client.get(
            "/api/user/get_by_id",
            params=params
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == User1_InDB


    async def test_read_multiple_users_OK(
        self,
        async_test_client,
        Users_List_Correct,
        monkeypatch
    ):  
        query_schema = jsonable_encoder(
            UserQueryOptionalSchema(
                height=1.90
            )
        )
        Users_Output = [users_dict["in_db"] for users_dict in Users_List_Correct]

        async def mock_read_optional(self, query_schema):
            return Users_Output
        monkeypatch.setattr(SQLAlchemyRepository, "read_optional", mock_read_optional)

        res = await async_test_client.post(
            "/api/user/get_optional",
            json=query_schema
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == Users_Output


    async def test_delete_user_OK(
        self,
        async_test_client,
        User1_Correct,
        monkeypatch
    ):  
        User1_InDB = User1_Correct["in_db"]
        params = {"id": 1}

        async def mock_delete(self, id):
            return User1_InDB
        monkeypatch.setattr(SQLAlchemyRepository, "delete", mock_delete)

        res = await async_test_client.delete(
            "/api/user/delete",
            params=params
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == User1_InDB

    


