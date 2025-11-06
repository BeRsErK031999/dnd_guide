import pytest
from domain.armor.armor import Armor
from domain.armor.armor_type import ArmorType
from domain.error import DomainError


@pytest.mark.parametrize(
    (
        "armor_type, name, description, armor_class_with_modifier, "
        "strength, stealth, weight, coins, should_error"
    ),
    [
        [
            ArmorType.LIGHT_ARMOR,
            "name",
            "description",
            [10, 3],
            1,
            True,
            10,
            10,
            False,
        ],
        [
            ArmorType.LIGHT_ARMOR,
            "",
            "description",
            [10, 3],
            1,
            True,
            10,
            10,
            True,
        ],
        [
            ArmorType.LIGHT_ARMOR,
            "name",
            "",
            [10, 3],
            1,
            True,
            10,
            10,
            True,
        ],
    ],
    indirect=["armor_class_with_modifier", "weight", "coins"],
)
def test_ok_create(
    gen_uuid,
    armor_type,
    name,
    description,
    armor_class_with_modifier,
    strength,
    stealth,
    weight,
    coins,
    should_error,
):
    try:
        Armor(
            gen_uuid(),
            armor_type,
            name,
            description,
            armor_class_with_modifier,
            strength,
            stealth,
            weight,
            coins,
        )
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "armor_type, should_error",
    [
        [ArmorType.LIGHT_ARMOR, True],
        [ArmorType.MEDIUM_ARMOR, False],
        [ArmorType.HEAVY_ARMOR, False],
        [ArmorType.SHIELD, False],
    ],
)
def test_change_armor_type(armor, armor_type, should_error):
    try:
        armor.new_armor_type(armor_type)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "name, should_error",
    [
        ["name", True],
        ["new_name", False],
        ["", True],
    ],
)
def test_change_name(armor, name, should_error):
    try:
        armor.new_name(name)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "description, should_error",
    [
        ["description", False],
        ["new_description", False],
        ["", True],
    ],
)
def test_change_description(armor, description, should_error):
    try:
        armor.new_description(description)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "armor_class_with_modifier, should_error",
    [
        [[10, 2], True],
        [[11, 2], False],
    ],
    indirect=["armor_class_with_modifier"],
)
def test_change_armor_class(armor, armor_class_with_modifier, should_error):
    try:
        armor.new_armor_class(armor_class_with_modifier)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "strength, should_error",
    [
        [-1, True],
        [10, False],
        [21, True],
    ],
)
def test_change_strength(armor, strength, should_error):
    try:
        armor.new_strength(strength)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")
