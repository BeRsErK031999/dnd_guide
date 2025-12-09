from typing import Sequence
from uuid import UUID, uuid4

from application.dto.model import (
    armor,
    character_class,
    character_subclass,
    class_feature,
    class_level,
    coin,
    dice,
    feat,
    game_time,
    length,
    material,
    material_component,
    race,
    source,
    spell,
    subclass_feature,
    subrace,
    tool,
    user,
    weapon,
    weapon_kind,
    weapon_property,
    weight,
)
from domain.armor import ArmorType
from domain.coin import PieceType
from domain.dice import DiceType
from domain.length import LengthUnit
from domain.modifier import Modifier
from domain.skill import Skill
from domain.weight import WeightUnit


def length_model_factory(
    count: float = 10, unit: str = LengthUnit.FT.name.lower()
) -> length.AppLength:
    return length.AppLength(count=count, unit=unit)


def dice_model_factory(
    count: int = 10, dice_type: str = DiceType.D10.name.lower()
) -> dice.AppDice:
    return dice.AppDice(count=count, dice_type=dice_type)


def weight_model_factory(
    count: float = 10, unit: str = WeightUnit.LB.name.lower()
) -> weight.AppWeight:
    return weight.AppWeight(count=count, unit=unit)


def coins_model_factory(
    count: int = 10, piece_type: str = PieceType.COPPER.name.lower()
) -> coin.AppCoins:
    return coin.AppCoins(count=count, piece_type=piece_type)


def armor_class_model_factory(
    base_class: int = 10,
    modifier: Modifier | None = None,
    max_modifier_bonus: int | None = None,
) -> armor.AppArmorClass:
    return armor.AppArmorClass(
        base_class=base_class, modifier=modifier, max_modifier_bonus=max_modifier_bonus
    )


def armor_model_factory(
    armor_id: UUID = uuid4(),
    armor_type: str = ArmorType.MEDIUM_ARMOR.name.lower(),
    name: str = "armor_name",
    description: str = "armor_description",
    strength: int = 15,
    stealth: bool = True,
    armor_class: armor.AppArmorClass = armor_class_model_factory(),
    armor_weight: weight.AppWeight = weight_model_factory(),
    cost: coin.AppCoins = coins_model_factory(),
    material_id: UUID = uuid4(),
) -> armor.AppArmor:
    return armor.AppArmor(
        armor_id=armor_id,
        armor_type=armor_type,
        name=name,
        description=description,
        armor_class=armor_class,
        strength=strength,
        stealth=stealth,
        weight=armor_weight,
        cost=cost,
        material_id=material_id,
    )


def class_hits_model_factory(
    hit_dice: dice.AppDice = dice_model_factory(),
    starting_hits: int = 10,
    hit_modifier: str = Modifier.CONSTITUTION.name.lower(),
    next_level_hits: int = 5,
) -> character_class.AppClassHits:
    return character_class.AppClassHits(
        hit_dice=hit_dice,
        starting_hits=starting_hits,
        hit_modifier=hit_modifier,
        next_level_hits=next_level_hits,
    )


def class_proficiencies_model_factory(
    armors: Sequence[str] = [
        ArmorType.LIGHT_ARMOR.name.lower(),
        ArmorType.MEDIUM_ARMOR.name.lower(),
    ],
    weapons: Sequence[UUID] = [],
    tools: Sequence[UUID] = [],
    saving_throws: Sequence[str] = [
        Modifier.STRENGTH.name.lower(),
        Modifier.CONSTITUTION.name.lower(),
    ],
    skills: Sequence[str] = [
        Skill.ATHLETICS.name.lower(),
        Skill.INTIMIDATION.name.lower(),
    ],
    number_skills: int = 2,
    number_tools: int = 1,
) -> character_class.AppClassProficiencies:
    return character_class.AppClassProficiencies(
        armors=armors,
        weapons=weapons,
        tools=tools,
        saving_throws=saving_throws,
        skills=skills,
        number_skills=number_skills,
        number_tools=number_tools,
    )


def class_model_factory(
    class_id: UUID = uuid4(),
    name: str = "class_name",
    description: str = "class_description",
    primary_modifiers: Sequence[str] = [Modifier.STRENGTH.name.lower()],
    hits: character_class.AppClassHits = class_hits_model_factory(),
    proficiencies: character_class.AppClassProficiencies = class_proficiencies_model_factory(),
    name_in_english: str = "class_name_in_english",
    source_id: UUID = uuid4(),
) -> character_class.AppClass:
    return character_class.AppClass(
        class_id=class_id,
        name=name,
        description=description,
        primary_modifiers=primary_modifiers,
        hits=hits,
        proficiencies=proficiencies,
        name_in_english=name_in_english,
        source_id=source_id,
    )


def subclass_model_factory(
    subclass_id: UUID = uuid4(),
    class_id: UUID = uuid4(),
    name: str = "subclass_name",
    description: str = "subclass_description",
    name_in_english: str = "subclass_name_english",
) -> character_subclass.AppSubclass:
    return character_subclass.AppSubclass(
        subclass_id=subclass_id,
        class_id=class_id,
        name=name,
        description=description,
        name_in_english=name_in_english,
    )


def class_feature_model_factory(
    feature_id: UUID = uuid4(),
    class_id: UUID = uuid4(),
    name: str = "feature_name",
    description: str = "feature_description",
    level: int = 1,
    name_in_english: str = "feature_name_english",
) -> class_feature.AppClassFeature:
    return class_feature.AppClassFeature(
        feature_id=feature_id,
        class_id=class_id,
        name=name,
        description=description,
        level=level,
        name_in_english=name_in_english,
    )


def class_level_dice_model_factory(
    hit_dice: dice.AppDice = dice_model_factory(),
    description: str = "class_level_dice_description",
) -> class_level.AppClassLevelDice:
    return class_level.AppClassLevelDice(dice=hit_dice, description=description)


def class_level_points_model_factory(
    points: int = 2, description: str = "class_level_points_description"
) -> class_level.AppClassLevelPoints:
    return class_level.AppClassLevelPoints(points=points, description=description)


def class_level_bonus_damage_model_factory(
    damage: int = 1,
    description: str = "class_level_bonus_damage_description",
) -> class_level.AppClassLevelBonusDamage:
    return class_level.AppClassLevelBonusDamage(damage=damage, description=description)


def class_level_increase_speed_model_factory(
    speed: length.AppLength = length_model_factory(),
    description: str = "class_level_increase_speed_description",
) -> class_level.AppClassLevelIncreaseSpeed:
    return class_level.AppClassLevelIncreaseSpeed(speed=speed, description=description)


def class_level_model_factory(
    class_level_id: UUID,
    class_id: UUID,
    level: int,
    dice: class_level.AppClassLevelDice | None = None,
    spell_slots: list[int] | None = None,
    number_cantrips_know: int | None = None,
    number_spells_know: int | None = None,
    number_arcanums_know: int | None = None,
    points: class_level.AppClassLevelPoints | None = None,
    bonus_damage: class_level.AppClassLevelBonusDamage | None = None,
    increase_speed: class_level.AppClassLevelIncreaseSpeed | None = None,
) -> class_level.AppClassLevel:
    return class_level.AppClassLevel(
        class_level_id=class_level_id,
        class_id=class_id,
        level=level,
        dice=dice,
        spell_slots=spell_slots,
        number_cantrips_know=number_cantrips_know,
        number_spells_know=number_spells_know,
        number_arcanums_know=number_arcanums_know,
        points=points,
        bonus_damage=bonus_damage,
        increase_speed=increase_speed,
    )


def material_model_factory(
    material_id: UUID = uuid4(),
    name: str = "material_name",
    description: str = "material_description",
) -> material.AppMaterial:
    return material.AppMaterial(
        material_id=material_id, name=name, description=description
    )


def user_model_factory(user_id: UUID = uuid4()) -> user.AppUser:
    return user.AppUser(user_id=user_id)
