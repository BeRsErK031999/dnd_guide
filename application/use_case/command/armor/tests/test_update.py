from uuid import uuid4

import pytest
from application.dto.command.armor import UpdateArmorCommand
from domain.armor import ArmorType
from domain.coin import PieceType
from domain.error import DomainError
from domain.modifier import Modifier
from domain.weight import WeightUnit


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_armor_command, armor_update_use_case, should_error",
    [
        [
            [
                True,
                ArmorType.LIGHT_ARMOR.name,
                "name",
                "description1",
                [11, Modifier.DEXTERITY.name, 2],
                2,
                False,
                [22, WeightUnit.LB.name],
                [22, PieceType.GOLD.name],
            ],
            ["other_name"],
            False,
        ],
        [
            [
                False,
                ArmorType.HEAVY_ARMOR.name,
                "name",
                "description",
                [10, Modifier.DEXTERITY.name, 2],
                0,
                True,
                [20, WeightUnit.LB.name],
                [20, PieceType.GOLD.name],
            ],
            ["other_name"],
            True,
        ],
        [
            [
                True,
                ArmorType.HEAVY_ARMOR.name,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            ["name"],
            True,
        ],
        [
            [
                True,
                None,
                "name",
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            ["name"],
            True,
        ],
        [
            [
                True,
                None,
                None,
                None,
                [10, Modifier.DEXTERITY.name, 2],
                None,
                None,
                None,
                None,
            ],
            ["name"],
            True,
        ],
        [
            [
                True,
                None,
                None,
                None,
                None,
                0,
                None,
                None,
                None,
            ],
            ["name"],
            True,
        ],
        [
            [
                True,
                None,
                None,
                None,
                None,
                None,
                True,
                None,
                None,
            ],
            ["name"],
            True,
        ],
        [
            [
                True,
                None,
                None,
                None,
                None,
                None,
                None,
                [20, WeightUnit.LB.name],
                None,
            ],
            ["name"],
            True,
        ],
        [
            [
                True,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                [20, PieceType.GOLD.name],
            ],
            ["name"],
            True,
        ],
    ],
    indirect=["update_armor_command", "armor_update_use_case"],
    ids=[
        "ok",
        "not_admin",
        "not_changed_type",
        "not_changed_name",
        "not_changed_class",
        "not_changed_strength",
        "not_changed_stealth",
        "not_changed_weight",
        "not_changed_cost",
    ],
)
async def test_update(update_armor_command, armor_update_use_case, should_error):
    try:
        await armor_update_use_case.execute(update_armor_command)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "armor_update_use_case",
    ["name"],
    indirect=["armor_update_use_case"],
)
async def test_armor_not_exists(armor_update_use_case, admin_user):
    with pytest.raises(DomainError):
        await armor_update_use_case.execute(
            UpdateArmorCommand(user_id=admin_user, armor_id=uuid4(), name="new_name")
        )
