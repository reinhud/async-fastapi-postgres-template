import datetime as dt

import pytest
from fastapi import status
from sqlalchemy import Column, DateTime

from sqlalchemy.sql import func

from app.db.models.base import BaseSaModel

from app.models.domain.user import UserCreate, UserUpdate, UserInDB
from app.db.repositories.base import SQLAlchemyRepository


@pytest.mark.anyio
class Test_User():

    async def test_create_user_OK(
        self,
        async_test_client,
        monkeypatch
    ):
        UPDATED_AT_DEFAULT = dt.datetime.now()
        User1_Create = UserCreate(
            name="Test User 1",
            height=1.90
        )
        User1_InDB = UserInDB(
                id=1,
                name="Test User 1",
                birthdate=None,
                height=1.90,
                updated_at=UPDATED_AT_DEFAULT
            )

        async def mock_post(self, obj_new):
            return User1_InDB         
        
        def mock_func_now() -> dt.datetime:
            return Column(DateTime, UPDATED_AT_DEFAULT)

        monkeypatch.setattr(SQLAlchemyRepository, "create", mock_post)
        monkeypatch.setattr(BaseSaModel, "updated_at", Column(DateTime, server_default=f"{UPDATED_AT_DEFAULT}"))
        
        res = await async_test_client.post(
            "/api/user/post",
            json=User1_Create.dict()
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == User1_InDB.dict()
        
    
    async def test_read_user_by_id_OK(
        self,
        async_test_client,
    ):  
        params = {"id": 1}
        res = await async_test_client.get(
            "/api/user/get_by_id",
            params=params
        )
        assert res.status_code == status.HTTP_200_OK

    async def test_read_user_optional_OK(
        self,
        async_test_client,
    ):  
        params = {"id": 1}
        res = await async_test_client.get(
            "/api/user/get_by_id",
            params=params
        )
        assert res.status_code == status.HTTP_200_OK

    async def test_delete_user_OK(
        self,
        async_test_client,
    ):  
        params = {"id": 1}
        res = await async_test_client.get(
            "/api/user/get_by_id",
            params=params
        )
        assert res.status_code == status.HTTP_200_OK

    


