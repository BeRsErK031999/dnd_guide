from typing import Sequence
from uuid import UUID, uuid4

from domain import (
    armor,
    character_class,
    character_subclass,
    class_feature,
    class_level,
    coin,
    creature_size,
    creature_type,
    damage_type,
    dice,
    feat,
    game_time,
    length,
    material,
    material_component,
    modifier,
    race,
    skill,
    source,
    spell,
    subclass_feature,
    subrace,
    tool,
    weapon,
    weapon_kind,
    weapon_property,
    weight,
)
from domain.modifier import Modifier


def game_time_factory(
    count: int = 1, units: game_time.GameTimeUnit = game_time.GameTimeUnit.ACTION
):
    return game_time.GameTime(count=count, units=units)


def dice_factory(count: int = 2, dice_type: dice.DiceType = dice.DiceType.D4):
    return dice.Dice(count=count, dice_type=dice_type)


def length_factory(count: int = 10, unit: length.LengthUnit = length.LengthUnit.FT):
    return length.Length(count=count, unit=unit)


def weight_factory(count: int = 1, unit: weight.WeightUnit = weight.WeightUnit.LB):
    return weight.Weight(
        count=count,
        unit=unit,
    )


def coin_factory():
    return coin.Coins(count=10, piece_type=coin.PieceType.COPPER)


def armor_class_factory(
    base_class: int = 10,
    modifier: Modifier | None = None,
    max_modifier_bonus: int | None = None,
):
    return armor.ArmorClass(
        base_class=base_class, modifier=modifier, max_modifier_bonus=max_modifier_bonus
    )


def armor_factory(
    armor_id: UUID = uuid4(),
    armor_type: armor.ArmorType = armor.ArmorType.HEAVY_ARMOR,
    name: str = "armor_name",
    description: str = "armor_description",
    armor_class: armor.ArmorClass = armor_class_factory(),
    strength: int = 15,
    stealth: bool = True,
    weight: weight.Weight = weight_factory(),
    cost: coin.Coins = coin_factory(),
    material_id: UUID = uuid4(),
):
    return armor.Armor(
        armor_id=armor_id,
        armor_type=armor_type,
        name=name,
        description=description,
        armor_class=armor_class,
        strength=strength,
        stealth=stealth,
        weight=weight,
        cost=cost,
        material_id=material_id,
    )


def class_hits_factory(
    hit_dice: dice.Dice = dice_factory(),
    starting_hits: int = 10,
    hit_modifier: Modifier = modifier.Modifier.CONSTITUTION,
    next_level_hits: int = 6,
):
    return character_class.ClassHits(
        hit_dice=hit_dice,
        starting_hits=starting_hits,
        hit_modifier=hit_modifier,
        next_level_hits=next_level_hits,
    )


def class_proficiencies_factory(
    armors: Sequence[armor.ArmorType] = [armor.ArmorType.HEAVY_ARMOR],
    weapons: Sequence[UUID] = [uuid4()],
    tools: Sequence[UUID] = [uuid4()],
    saving_throws: Sequence[Modifier] = [modifier.Modifier.CHARISMA],
    skills: Sequence[skill.Skill] = [skill.Skill.ACROBATICS],
    number_skills: int = 1,
    number_tools: int = 1,
):
    return character_class.ClassProficiencies(
        armors=armors,
        weapons=weapons,
        tools=tools,
        saving_throws=saving_throws,
        skills=skills,
        number_skills=number_skills,
        number_tools=number_tools,
    )


def class_factory(
    class_id: UUID = uuid4(),
    name: str = "class_name",
    description: str = "class_description",
    primary_modifiers: Sequence[Modifier] = [modifier.Modifier.CHARISMA],
    hits: character_class.ClassHits = class_hits_factory(),
    proficiencies: character_class.ClassProficiencies = class_proficiencies_factory(),
    name_in_english: str = "class_name_in_english",
    source_id: UUID = uuid4(),
):
    return character_class.CharacterClass(
        class_id=class_id,
        name=name,
        description=description,
        primary_modifiers=primary_modifiers,
        hits=hits,
        proficiencies=proficiencies,
        name_in_english=name_in_english,
        source_id=source_id,
    )
