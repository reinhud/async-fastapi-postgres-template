import pytest
from fastapi import status

from app.models.domain.user import UserCreate


class Test_User():

    @pytest.mark.anyio
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

    @pytest.mark.anyio
    async def test_create_user_OK(
        self,
        async_test_client,
    ):
        user1 = {"name":"Test User 1"}
        
        res = await async_test_client.post(
            "/api/user/post",
            json=user1
        )
        assert res.status_code == status.HTTP_201_CREATED


