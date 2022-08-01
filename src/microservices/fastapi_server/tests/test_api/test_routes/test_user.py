import datetime as dt

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from fastapi import status

from app.models.domain.user import UserCreate

@pytest.mark.anyio
class Test_Users:
    # All test coroutines will be treated as marked.

    async def test_create_user(
        self,  
        async_test_client: AsyncClient, 
        user1: UserCreate
    ) -> None:
        new_user = {
        "name":"User 1",
        "birthdate":str(dt.date(2000, 1, 1)),
        "wealth":1
        }
        response = await async_test_client.post(
            "/api/user/user/post",
            json=new_user
        )
        assert response.status_code == status.HTTP_201_CREATED
        #data = response.json()
        #assert data["name"] == "User 1"
        #user_id = data["id"]'''

        



