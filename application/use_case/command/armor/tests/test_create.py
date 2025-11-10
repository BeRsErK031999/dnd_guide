import pytest
from domain.armor import ArmorType
from domain.coin import PieceType
from domain.error import DomainError
from domain.modifier import Modifier
from domain.weight import WeightUnit


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_armor_command, armor_create_use_case, should_error",
    [
        [
            [
                True,
                ArmorType.HEAVY_ARMOR.name,
                "name",
                "description",
                [10, Modifier.DEXTERITY.name, 2],
                1,
                True,
                [20, WeightUnit.LB.name],
                [20, PieceType.GOLD.name],
            ],
            [""],
            False,
        ],
        [
            [
                True,
                ArmorType.HEAVY_ARMOR.name,
                "name",
                "description",
                [10, None, None],
                1,
                True,
                [20, WeightUnit.LB.name],
                [20, PieceType.GOLD.name],
            ],
            [""],
            False,
        ],
        [
            [
                False,
                ArmorType.HEAVY_ARMOR.name,
                "name",
                "description",
                [10, Modifier.DEXTERITY.name, 2],
                1,
                True,
                [20, WeightUnit.LB.name],
                [20, PieceType.GOLD.name],
            ],
            [""],
            True,
        ],
        [
            [
                True,
                ArmorType.HEAVY_ARMOR.name,
                "name",
                "description",
                [10, Modifier.DEXTERITY.name, 2],
                1,
                True,
                [20, WeightUnit.LB.name],
                [20, PieceType.GOLD.name],
            ],
            ["name"],
            True,
        ],
    ],
    indirect=["create_armor_command", "armor_create_use_case"],
    ids=["ok_with_modifier", "ok_without_modifier", "not_admin", "duplicate_name"],
)
async def test_create(create_armor_command, armor_create_use_case, should_error):
    try:
        await armor_create_use_case.execute(create_armor_command)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")
