import pytest
from fastapi import status

from app.core.config import get_app_settings


@pytest.mark.anyio
async def test_root(async_test_client):
    """Test if app is available"""
    res = await async_test_client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"message": "OK"}


class Test_Settings:
    """Checking correct settings for testing are used."""
    
    def test_correct_app_env(self):
        """Check that correct environment is enabled for test suite."""

        assert get_app_settings().app_env == "prod"

    def test_correct_testing_db(self):
        """Test that right database is used for testing"""
        TEST_DATABASE = "postgresql+asyncpg://postgres:Start123@postgres_container:5432/main_db"

        assert get_app_settings().database_url == TEST_DATABASE