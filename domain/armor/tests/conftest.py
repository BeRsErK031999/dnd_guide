from uuid import uuid4

import pytest
from domain.armor.armor import Armor
from domain.armor.armor_class import ArmorClass
from domain.armor.armor_type import ArmorType
from domain.coin import Coins, PieceType
from domain.modifier import Modifier
from domain.weight import Weight, WeightUnit


@pytest.fixture
def gen_uuid():
    return uuid4


@pytest.fixture
def weight(request: pytest.FixtureRequest) -> Weight:
    return Weight(float(request.param), WeightUnit.LB)


@pytest.fixture
def coins(request: pytest.FixtureRequest) -> Coins:
    return Coins(int(request.param), PieceType.GOLD)


@pytest.fixture
def armor_class_with_modifier(request: pytest.FixtureRequest) -> ArmorClass:
    kd, bonus = request.param
    return ArmorClass(int(kd), Modifier.DEXTERITY, int(bonus))


@pytest.fixture
def armor_class_without_modifier(request: pytest.FixtureRequest) -> ArmorClass:
    return ArmorClass(int(request.param), None, None)


@pytest.fixture
def armor(gen_uuid) -> Armor:
    return Armor(
        gen_uuid(),
        ArmorType.LIGHT_ARMOR,
        "name",
        "description",
        ArmorClass(10, Modifier.DEXTERITY, 2),
        0,
        False,
        Weight(10, WeightUnit.LB),
        Coins(10, PieceType.GOLD),
    )
