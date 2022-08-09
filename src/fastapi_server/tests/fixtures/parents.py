import datetime as dt
from typing import List

from fastapi.encoders import jsonable_encoder
import pytest

from app.models.domain.parents import ParentCreate, ParentInDB


## ===== Valid Parent 1 ===== ##
@pytest.fixture
def Parent1_Create() -> ParentCreate:
    """Returns a json compatible dict of example ParentCreate model"""
    parent = ParentCreate(
        name="Test Parent 1",
        height=1.90
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent1_InDB() -> ParentCreate:
    """Returns a json compatible dict of example ParentInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    parent = ParentInDB(
        id=1,
        name="Test Parent 1",
        birthdate=None,
        height=1.90,
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent1_Correct(Parent1_Create, Parent1_InDB):
    parent1_schemas = {
        "create": Parent1_Create,
        "in_db": Parent1_InDB,
    }
    return parent1_schemas

## ====== Valid Parent 2 ===== ##
@pytest.fixture
def Parent2_Create() -> ParentCreate:
    """Returns a json compatible dict of example ParentCreate model"""
    parent = ParentCreate(
        name="Test Parent 2",
        height=1.90
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent2_InDB() -> ParentCreate:
    """Returns a json compatible dict of example ParentInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    parent = ParentInDB(
        id=2,
        name="Test Parent 2",
        birthdate=None,
        height=1.90,
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent2_Correct(Parent2_Create, Parent2_InDB):
    parent2_schemas = {
        "create": Parent2_Create,
        "in_db": Parent2_InDB,
    }
    return parent2_schemas


## ===== Valid Parents List ===== ##
@pytest.fixture
def Parents_List_Correct(Parent1_Correct, Parent2_Correct):
    parents_list: List[dict, dict] = [Parent1_Correct, Parent2_Correct]
    return parents_list