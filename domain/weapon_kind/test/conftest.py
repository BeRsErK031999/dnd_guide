from uuid import uuid4

import pytest
from domain.weapon_kind.weapon_kind import WeaponKind


@pytest.fixture
def gen_uuid():
    return uuid4


@pytest.fixture
def weapon_kind(gen_uuid, request) -> WeaponKind:
    weapon_type, name, description = request.param
    return WeaponKind(gen_uuid(), name, description, weapon_type)
