import pytest
from fastapi import status

from app.models.domain.user import UserCreate


class Test_User():
    @pytest.mark.anyio
    async def test_create_user_OK(async_test_client):
        user1 = {"name":"Test User 1"}
        
        res = await async_test_client.post(
            "/api/user/user/post",
            json=user1
        )
        assert res.status_code == 201


    @pytest.mark.anyio
    async def test_get_user_OK(async_test_client):
        user1 = {"name":"Test User 1"}
        
        res = await async_test_client.post(
            "/api/user/user/post",
            json=user1
        )
        assert res.status_code == 200

