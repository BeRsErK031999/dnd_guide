from uuid import uuid4

import pytest
from domain.length import Length, LengthUnit
from domain.weapon_property.weapon_property import WeaponProperty


@pytest.fixture
def gen_uuid():
    return uuid4


@pytest.fixture
def base_attack_range(request) -> Length | None:
    val = request.param
    if val is None:
        return None
    return Length(float(val), LengthUnit.FT)


@pytest.fixture
def max_attack_range(request) -> Length | None:
    val = request.param
    if val is None:
        return None
    return Length(float(val), LengthUnit.FT)


@pytest.fixture
def weapon_property(gen_uuid, request) -> WeaponProperty:
    name, base_range, max_range, second_hand = request.param
    if base_range is not None:
        base_range = Length(base_range, LengthUnit.FT)
    if max_range is not None:
        max_range = Length(max_range, LengthUnit.FT)
    return WeaponProperty(
        gen_uuid(), name, "description", base_range, max_range, second_hand
    )
