"""Fixtures for testing 'parent' ressource."""
import datetime as dt
from typing import List

from fastapi.encoders import jsonable_encoder
import pytest

from app.db.models.parents import Parent as ParentModel
from app.models.domain.parents import ParentCreate, ParentInDB


## ===== Valid Parent 1 ===== ##
@pytest.fixture
def Parent1_Create() -> ParentCreate:
    """Returns a json compatible dict of example ParentCreate model"""
    parent = ParentCreate(
        name="Parent 1",
        birthdate=dt.datetime(1980, 1, 1),
        height=1.90,  
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent1_InDB_Schema() -> ParentCreate:
    """Returns a json compatible dict of example ParentInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    parent = ParentInDB(
        id=1,
        name="Parent 1",
        birthdate=dt.datetime(1980, 1, 1),
        height=1.90, 
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent1_InDB_Model(Parent1_InDB_Schema) -> ParentModel:
    return ParentModel(**Parent1_InDB_Schema.dict())


## ====== Valid Parent 2 ===== ##
@pytest.fixture
def Parent2_Create() -> ParentCreate:
    """Returns a json compatible dict of example ParentCreate model"""
    parent = ParentCreate(
        name="Parent 2",
        birthdate=dt.datetime(1985, 1, 1),
        height=1.90, 
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent2_InDB_Schema() -> ParentCreate:
    """Returns a json compatible dict of example ParentInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    parent = ParentInDB(
        id=2,
        name="Parent 2",
        birthdate=dt.datetime(1985, 1, 1),
        height=1.90, 
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent2_InDB_Model(Parent2_InDB_Schema) -> ParentModel:
    return ParentModel(**Parent2_InDB_Schema.dict())


## ====== Valid Parent 3 ===== ##
@pytest.fixture
def Parent3_Create() -> ParentCreate:
    """Returns a json compatible dict of example ParentCreate model"""
    parent = ParentCreate(
        name="New Parent 3",
        birthdate=dt.datetime(1970, 1, 1),
        height=1.75, 
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent3_InDB_Schema() -> ParentCreate:
    """Returns a json compatible dict of example ParentInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    parent = ParentInDB(
        id=3,
        name="New Parent 3",
        birthdate=dt.datetime(1970, 1, 1),
        height=1.75,
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(parent)

@pytest.fixture
def Parent3_InDB_Model(Parent3_InDB_Schema) -> ParentModel:
    return ParentModel(**Parent3_InDB_Schema.dict())