import pytest
from domain.damage_type import DamageType
from domain.dice import Dice
from domain.error import DomainError
from domain.weapon.weapon import Weapon


@pytest.mark.parametrize(
    "name, description, coins, weapon_damage, weight, should_error",
    [
        ["name", "description", 20, [Dice.D10, DamageType.ACID, 0], 5, False],
        ["name", "", 20, [Dice.D10, DamageType.ACID, 0], 5, True],
        ["", "description", 20, [Dice.D10, DamageType.ACID, 0], 5, True],
    ],
    indirect=["coins", "weapon_damage", "weight"],
)
def test_create(
    gen_uuid, name, description, coins, weapon_damage, weight, should_error
):
    try:
        Weapon(
            gen_uuid(),
            gen_uuid(),
            name,
            description,
            coins,
            weapon_damage,
            weight,
            [gen_uuid(), gen_uuid()],
        )
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "weapon, name, should_error",
    [
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            "new_name",
            False,
        ],
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            "name",
            True,
        ],
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            "",
            True,
        ],
    ],
    indirect=["weapon"],
)
def test_change_name(weapon, name, should_error):
    try:
        weapon.new_name(name)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert weapon.name() == name


@pytest.mark.parametrize(
    "weapon, description, should_error",
    [
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            "new_description",
            False,
        ],
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            "description",
            False,
        ],
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            "",
            True,
        ],
    ],
    indirect=["weapon"],
)
def test_change_description(weapon, description, should_error):
    try:
        weapon.new_description(description)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert weapon.description() == description


@pytest.mark.parametrize(
    "weapon, coins, should_error",
    [
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            25,
            False,
        ],
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            20,
            True,
        ],
    ],
    indirect=["weapon", "coins"],
)
def test_change_cost(weapon, coins, should_error):
    try:
        weapon.new_cost(coins)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert weapon.cost() == coins


@pytest.mark.parametrize(
    "weapon, weight, should_error",
    [
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            2,
            False,
        ],
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            5,
            True,
        ],
    ],
    indirect=["weapon", "weight"],
)
def test_change_weight(weapon, weight, should_error):
    try:
        weapon.new_weight(weight)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert weapon.weight() == weight


@pytest.mark.parametrize(
    "weapon, weapon_damage, should_error",
    [
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            [Dice.D12, DamageType.ACID, 0],
            False,
        ],
        [
            ["name", "description", 20, Dice.D10, DamageType.ACID, 0, 5],
            [Dice.D10, DamageType.ACID, 0],
            True,
        ],
    ],
    indirect=["weapon", "weapon_damage"],
)
def test_change_damage(weapon, weapon_damage, should_error):
    try:
        weapon.new_damage(weapon_damage)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert weapon.damage() == weapon_damage
