import datetime as dt
from typing import List

from fastapi.encoders import jsonable_encoder
import pytest

from app.models.domain.user import UserCreate, UserInDB


## ===== Valid User 1 ===== ##
@pytest.fixture
def User1_Create() -> UserCreate:
    """Returns a json compatible dict of example UserCreate model"""
    user = UserCreate(
        name="Test User 1",
        height=1.90
    )
    return jsonable_encoder(user)

@pytest.fixture
def User1_InDB() -> UserCreate:
    """Returns a json compatible dict of example UserInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    user = UserInDB(
        id=1,
        name="Test User 1",
        birthdate=None,
        height=1.90,
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(user)

@pytest.fixture
def User1_Correct(User1_Create, User1_InDB):
    user1_schemas = {
        "create": User1_Create,
        "in_db": User1_InDB,
    }
    return user1_schemas

## ====== Valid User 2 ===== ##
@pytest.fixture
def User2_Create() -> UserCreate:
    """Returns a json compatible dict of example UserCreate model"""
    user = UserCreate(
        name="Test User 2",
        height=1.90
    )
    return jsonable_encoder(user)

@pytest.fixture
def User2_InDB() -> UserCreate:
    """Returns a json compatible dict of example UserInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    user = UserInDB(
        id=2,
        name="Test User 2",
        birthdate=None,
        height=1.90,
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(user)

@pytest.fixture
def User2_Correct(User2_Create, User2_InDB):
    user2_schemas = {
        "create": User2_Create,
        "in_db": User2_InDB,
    }
    return user2_schemas


## ===== Valid Users List ===== ##
@pytest.fixture
def Users_List_Correct(User1_Correct, User2_Correct):
    users_list: List[dict, dict] = [User1_Correct, User2_Correct]
    return users_list