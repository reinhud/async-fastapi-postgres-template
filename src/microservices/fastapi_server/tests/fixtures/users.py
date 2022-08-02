import pytest


from app.models.domain.user import UserCreate


@pytest.fixture
def user1_create_correct():
    user = UserCreate(
        name="Test User 1",
        height=1.90
    )