import pytest
from sqlalchemy_utils import database_exists

from app.core.config import get_app_settings


@pytest.mark.asyncio
class Test_Settings:
    """Testing if test environment was used for spinning up tests."""
    def test_correct_app_env(self):
        """Check that correct environment is enabled for test suite."""

        assert get_app_settings().app_env == "test"

    def test_correct_testing_db(self):
        """Test that right database is used for testing"""
        TEST_DATABASE = "postgresql+asyncpg://postgres:Start123@data_warehouse_test:5432/main_db_test"

        assert get_app_settings().database_url == TEST_DATABASE

    def test_database_exists(self):
        exists = database_exists(get_app_settings().database_url)
        exists == "True"


