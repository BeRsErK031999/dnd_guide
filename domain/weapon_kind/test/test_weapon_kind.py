import pytest
from domain.error import DomainError
from domain.weapon_kind.weapon_kind import WeaponKind
from domain.weapon_kind.weapon_type import WeaponType


@pytest.mark.parametrize(
    "weapon_type, name, description, should_error",
    [
        [WeaponType.MARTIAL_MELEE, "name", "description", False],
        [WeaponType.MARTIAL_MELEE, "name", "", True],
        [WeaponType.MARTIAL_MELEE, "", "description", True],
        [WeaponType.MARTIAL_MELEE, "", "", True],
    ],
)
def test_create(gen_uuid, weapon_type, name, description, should_error):
    try:
        WeaponKind(gen_uuid, name, description, weapon_type)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "weapon_kind, name, should_error",
    [
        [[WeaponType.MARTIAL_MELEE, "name", "description"], "new_name", False],
        [[WeaponType.MARTIAL_MELEE, "name", "description"], "name", True],
        [[WeaponType.MARTIAL_MELEE, "name", "description"], "", True],
    ],
    indirect=["weapon_kind"],
)
def test_change_name(weapon_kind, name, should_error):
    try:
        weapon_kind.new_name(name)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert weapon_kind.name() == name


@pytest.mark.parametrize(
    "weapon_kind, description, should_error",
    [
        [[WeaponType.MARTIAL_MELEE, "name", "description"], "new_description", False],
        [[WeaponType.MARTIAL_MELEE, "name", "description"], "description", False],
        [[WeaponType.MARTIAL_MELEE, "name", "description"], "", True],
    ],
    indirect=["weapon_kind"],
)
def test_change_description(weapon_kind, description, should_error):
    try:
        weapon_kind.new_description(description)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert weapon_kind.description() == description


@pytest.mark.parametrize(
    "weapon_kind, weapon_type, should_error",
    [
        [
            [WeaponType.MARTIAL_MELEE, "name", "description"],
            WeaponType.MARTIAL_RANGE,
            False,
        ],
        [
            [WeaponType.MARTIAL_MELEE, "name", "description"],
            WeaponType.MARTIAL_MELEE,
            True,
        ],
    ],
    indirect=["weapon_kind"],
)
def test_change_type(weapon_kind, weapon_type, should_error):
    try:
        weapon_kind.new_weapon_type(weapon_type)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert weapon_kind.weapon_type() == weapon_type
