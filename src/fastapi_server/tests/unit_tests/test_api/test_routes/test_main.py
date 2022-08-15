"""Testing endpoints defined in main."""
from fastapi import status
import pytest

from app.core.config import get_app_settings


@pytest.mark.anyio
class Test_Main:
    """Test class for app info endpoints defined in main."""
    async def test_root(self, async_test_client):
        """Test if app is available."""
        res = await async_test_client.get("/")
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == {"message": "OK"}
