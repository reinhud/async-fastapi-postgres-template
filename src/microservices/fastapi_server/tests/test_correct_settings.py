'''from app.core.config import get_app_settings


def test_correct_app_env():
    """Check that correct environment is enabled for test suite."""

    assert get_app_settings().app_env == "test"


def test_correct_testing_db():
    """Test that right database is used for testing"""
    TEST_DATABASE = "postgresql+asyncpg://postgres:Start123@postgres_test_container:5432/main_db_test"

    assert get_app_settings().database_url == TEST_DATABASE'''

def test_dummy():
    a = 1 + 2

    assert a == 3