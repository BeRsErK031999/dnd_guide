import pytest
from domain.dice import Dice, DiceType
from domain.error import DomainError
from domain.weapon_property.name import WeaponPropertyName
from domain.weapon_property.weapon_property import WeaponProperty


@pytest.mark.parametrize(
    "name, description, base_attack_range, max_attack_range, second_hand_dice, should_error",
    [
        [WeaponPropertyName.AMMUNITION, "description", 20, 40, None, False],
        [
            WeaponPropertyName.VERSATILE,
            "description",
            None,
            None,
            Dice(1, DiceType.D10),
            False,
        ],
        [WeaponPropertyName.DISTANCE, "description", None, None, None, False],
        [WeaponPropertyName.DISTANCE, "description", 20, None, None, True],
        [WeaponPropertyName.DISTANCE, "description", 20, 40, None, True],
        [
            WeaponPropertyName.DISTANCE,
            "description",
            20,
            40,
            Dice(1, DiceType.D10),
            True,
        ],
        [
            WeaponPropertyName.DISTANCE,
            "description",
            None,
            40,
            Dice(1, DiceType.D10),
            True,
        ],
        [
            WeaponPropertyName.DISTANCE,
            "description",
            None,
            None,
            Dice(1, DiceType.D10),
            True,
        ],
        [
            WeaponPropertyName.DISTANCE,
            "description",
            20,
            None,
            Dice(1, DiceType.D10),
            True,
        ],
        [
            WeaponPropertyName.AMMUNITION,
            "description",
            20,
            40,
            Dice(1, DiceType.D10),
            True,
        ],
        [WeaponPropertyName.AMMUNITION, "description", None, 40, None, True],
        [WeaponPropertyName.AMMUNITION, "description", None, None, None, True],
        [WeaponPropertyName.VERSATILE, "description", None, None, None, True],
        [
            WeaponPropertyName.VERSATILE,
            "description",
            None,
            40,
            Dice(1, DiceType.D10),
            True,
        ],
        [
            WeaponPropertyName.VERSATILE,
            "description",
            20,
            40,
            Dice(1, DiceType.D10),
            True,
        ],
    ],
    indirect=["base_attack_range", "max_attack_range"],
)
def test_create(
    gen_uuid,
    name,
    description,
    base_attack_range,
    max_attack_range,
    second_hand_dice,
    should_error,
):
    try:
        WeaponProperty(
            gen_uuid(),
            name,
            description,
            base_attack_range,
            max_attack_range,
            second_hand_dice,
        )
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "weapon_property, name, base_attack_range, max_attack_range, second_hand_dice, should_error",
    [
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            WeaponPropertyName.DISTANCE,
            None,
            None,
            None,
            False,
        ],
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            WeaponPropertyName.VERSATILE,
            None,
            None,
            Dice(1, DiceType.D10),
            False,
        ],
        [
            [WeaponPropertyName.VERSATILE, None, None, Dice(1, DiceType.D10)],
            WeaponPropertyName.AMMUNITION,
            20,
            40,
            None,
            False,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.AMMUNITION,
            20,
            40,
            None,
            False,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.AMMUNITION,
            None,
            None,
            None,
            True,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.AMMUNITION,
            20,
            None,
            None,
            True,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.AMMUNITION,
            None,
            40,
            None,
            True,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.AMMUNITION,
            None,
            40,
            Dice(1, DiceType.D10),
            True,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.VERSATILE,
            None,
            40,
            None,
            True,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.FINESSE,
            None,
            40,
            None,
            True,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.FINESSE,
            None,
            None,
            Dice(1, DiceType.D10),
            True,
        ],
        [
            [WeaponPropertyName.DISTANCE, None, None, None],
            WeaponPropertyName.DISTANCE,
            None,
            None,
            None,
            True,
        ],
    ],
    indirect=["weapon_property", "base_attack_range", "max_attack_range"],
)
def test_change_name(
    weapon_property,
    name,
    base_attack_range,
    max_attack_range,
    second_hand_dice,
    should_error,
):
    try:
        weapon_property.new_name(
            name,
            base_range=base_attack_range,
            max_range=max_attack_range,
            second_hand_dice=second_hand_dice,
        )
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "weapon_property, description, should_error",
    [
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            "description",
            False,
        ],
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            "new_description",
            False,
        ],
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            "",
            True,
        ],
    ],
    indirect=["weapon_property"],
)
def test_change_description(weapon_property, description, should_error):
    try:
        weapon_property.new_description(description)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "weapon_property, base_attack_range, should_error",
    [
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            20,
            True,
        ],
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            10,
            False,
        ],
        [
            [WeaponPropertyName.VERSATILE, None, None, Dice(1, DiceType.D10)],
            10,
            True,
        ],
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            50,
            True,
        ],
    ],
    indirect=["weapon_property", "base_attack_range"],
)
def test_change_base_range(weapon_property, base_attack_range, should_error):
    try:
        weapon_property.new_base_range(base_attack_range)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "weapon_property, max_attack_range, should_error",
    [
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            40,
            True,
        ],
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            30,
            False,
        ],
        [
            [WeaponPropertyName.VERSATILE, None, None, Dice(1, DiceType.D10)],
            10,
            True,
        ],
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            10,
            True,
        ],
    ],
    indirect=["weapon_property", "max_attack_range"],
)
def test_change_max_range(weapon_property, max_attack_range, should_error):
    try:
        weapon_property.new_max_range(max_attack_range)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "weapon_property, second_hand_dice, should_error",
    [
        [
            [WeaponPropertyName.AMMUNITION, 20, 40, None],
            Dice(1, DiceType.D10),
            True,
        ],
        [
            [WeaponPropertyName.VERSATILE, None, None, Dice(1, DiceType.D10)],
            Dice(1, DiceType.D12),
            False,
        ],
        [
            [WeaponPropertyName.VERSATILE, None, None, Dice(1, DiceType.D10)],
            Dice(1, DiceType.D10),
            True,
        ],
    ],
    indirect=["weapon_property"],
)
def test_change_second_hand_dice(weapon_property, second_hand_dice, should_error):
    try:
        weapon_property.new_second_hand_dice(second_hand_dice)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")
