import pytest

from app.models.domain.user import UserCreate


@pytest.fixture
def user1_create_correct() -> UserCreate:
    user = UserCreate(
        name="Test User 1",
        height=1.90
    )
    return user