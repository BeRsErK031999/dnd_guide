from uuid import uuid4

import pytest
from domain import error
from domain.armor.armor_type import ArmorType
from domain.modifier import Modifier
from tests.factories import domain_factory

st_armor = domain_factory.armor_factory()


@pytest.mark.parametrize(
    "fields",
    [
        {"base_class": 14, "modifier": None, "max_modifier_bonus": None},
        {"base_class": 14, "modifier": Modifier.CHARISMA, "max_modifier_bonus": 2},
    ],
    ids=[
        "armor_class_without_modifier",
        "armor_class_with_modifier",
    ],
)
def test_create_armor_class_ok(fields):
    domain_factory.armor_class_factory(**fields)


@pytest.mark.parametrize(
    "fields",
    [
        {"base_class": 25, "modifier": None, "max_modifier_bonus": None},
        {"base_class": -1, "modifier": None, "max_modifier_bonus": None},
        {"base_class": 15, "modifier": None, "max_modifier_bonus": 5},
        {"base_class": 15, "modifier": Modifier.CHARISMA, "max_modifier_bonus": -1},
    ],
    ids=[
        "class_more_then_20",
        "class_less_then_0",
        "without_modifier_bonus",
        "modifier_bonus_less_then_0",
    ],
)
def test_create_armor_class_invalid(fields):
    try:
        domain_factory.armor_class_factory(**fields)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


def test_create_ok():
    domain_factory.armor_factory()


@pytest.mark.parametrize(
    "fields",
    [{"strength": -1}, {"strength": 21}],
    ids=["strength_is_0", "strength_is_21"],
)
def test_create_invalid(fields):
    try:
        domain_factory.armor_factory(**fields)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.parametrize(
    "set_method,get_method,value,expected_error",
    [
        [
            "new_armor_type",
            "armor_type",
            st_armor.armor_type(),
            error.DomainErrorStatus.IDEMPOTENT,
        ],
        ["new_armor_type", "armor_type", ArmorType.MEDIUM_ARMOR, None],
        [
            "new_armor_class",
            "armor_class",
            st_armor.armor_class(),
            error.DomainErrorStatus.IDEMPOTENT,
        ],
        [
            "new_armor_class",
            "armor_class",
            domain_factory.armor_class_factory(base_class=16),
            None,
        ],
        [
            "new_strength",
            "strength",
            st_armor.strength(),
            error.DomainErrorStatus.IDEMPOTENT,
        ],
        ["new_strength", "strength", 25, error.DomainErrorStatus.INVALID_DATA],
        ["new_strength", "strength", -1, error.DomainErrorStatus.INVALID_DATA],
        ["new_strength", "strength", st_armor.strength() + 1, None],
        [
            "new_stealth",
            "stealth",
            st_armor.stealth(),
            error.DomainErrorStatus.IDEMPOTENT,
        ],
        ["new_stealth", "stealth", not st_armor.stealth(), None],
        ["new_weight", "weight", st_armor.weight(), error.DomainErrorStatus.IDEMPOTENT],
        ["new_weight", "weight", domain_factory.weight_factory(count=30), None],
        ["new_cost", "cost", st_armor.cost(), error.DomainErrorStatus.IDEMPOTENT],
        [
            "new_cost",
            "cost",
            domain_factory.coin_factory(count=st_armor.cost().in_copper() + 10),
            None,
        ],
        [
            "new_material_id",
            "material_id",
            st_armor.material_id(),
            error.DomainErrorStatus.IDEMPOTENT,
        ],
        ["new_material_id", "material_id", uuid4(), None],
    ],
    ids=[
        "invalid_armor_type",
        "valid_armor_type",
        "invalid_armor_class",
        "valid_armor_class",
        "same_strength",
        "strength_is_25",
        "strength_is_0",
        "valid_strength",
        "invalid_stealth",
        "valid_stealth",
        "invalid_weight",
        "valid_weight",
        "invalid_cost",
        "valid_cost",
        "invalid_material_id",
        "valid_material_id",
    ],
)
def test_update(set_method, get_method, value, expected_error):
    armor = domain_factory.armor_factory()
    try:
        getattr(armor, set_method)(value)
    except error.DomainError as e:
        if expected_error is not None:
            assert e.status == expected_error
            return
        raise e
    assert getattr(armor, get_method)() == value
