from uuid import uuid4

import pytest
from domain.coin import Coins, PieceType
from domain.weapon.damage import WeaponDamage
from domain.weapon.weapon import Weapon
from domain.weight import Weight, WeightUnit


@pytest.fixture
def gen_uuid():
    return uuid4


@pytest.fixture
def weapon_damage(request) -> WeaponDamage:
    dice, damage_type, bonus = request.param
    return WeaponDamage(dice, damage_type, bonus)


@pytest.fixture
def weight(request: pytest.FixtureRequest) -> Weight:
    return Weight(float(request.param), WeightUnit.LB)


@pytest.fixture
def coins(request: pytest.FixtureRequest) -> Coins:
    return Coins(int(request.param), PieceType.GOLD)


@pytest.fixture
def weapon(gen_uuid, request) -> Weapon:
    name, description, cost, dice, damage_type, bonus, weight = request.param
    cost = Coins(cost, PieceType.GOLD)
    weight = Weight(weight, WeightUnit.LB)
    damage = WeaponDamage(dice, damage_type, bonus)
    return Weapon(
        gen_uuid(),
        gen_uuid(),
        name,
        description,
        cost,
        damage,
        weight,
        [gen_uuid(), gen_uuid()],
        uuid4(),
    )
