"""Fixtures for testing 'child' ressource."""
import datetime as dt

from fastapi.encoders import jsonable_encoder
import pytest

from app.db.models.children import Child as ChildModel
from app.models.domain.children import ChildCreate, ChildInDB


## ===== Valid Child 1 ===== ##
@pytest.fixture
def Child1_Create_Schema() -> ChildCreate:
    """Returns a json compatible dict of example ChildCreate model"""
    child = ChildCreate(
        name="Child 1",
        birthdate=dt.datetime(2000, 1, 1),
        height=1.80,
        hobby="Computer Science",
        parent_id=1
    )
    return jsonable_encoder(child)

@pytest.fixture
def Child1_InDB_Schema() -> ChildInDB:
    """Returns a json compatible dict of example ChildInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    child = ChildInDB(
        id=1,
        name="Child 1",
        birthdate=dt.datetime(2000, 1, 1),
        height=1.80,
        hobby="Computer Science",
        parent_id=1,
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(child)

@pytest.fixture
def Child1_InDB_Model(Child1_InDB_Schema) -> ChildModel:
    return ChildModel(**Child1_InDB_Schema.dict())


## ===== Valid Child 2 ===== ##
@pytest.fixture
def Child2_Create() -> ChildCreate:
    """Returns a json compatible dict of example ChildCreate model"""
    child = ChildCreate(
        name="Child 2",
        birthdate=dt.datetime(2005, 1, 1),
        height=1.70,
        hobby="Bouldering",
        parent_id=1
    )
    return jsonable_encoder(child)

@pytest.fixture
def Child2_InDB_Schema() -> ChildInDB:
    """Returns a json compatible dict of example ChildInDB model"""
    UPDATED_AT_DEFAULT = dt.datetime.now()
    child = ChildInDB(
        id=2,
        name="Child 2",
        birthdate=dt.datetime(2005, 1, 1),
        height=1.70,
        hobby="Bouldering",
        parent_id=1,
        updated_at=UPDATED_AT_DEFAULT
    )
    return jsonable_encoder(child)

@pytest.fixture
def Child2_InDB_Model(Child2_InDB_Schema) -> ChildModel:
    return ChildModel(**Child2_InDB_Schema.dict())