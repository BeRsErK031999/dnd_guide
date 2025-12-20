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
    modifier: modifier.Modifier | None = None,
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
    hit_modifier: modifier.Modifier = modifier.Modifier.CONSTITUTION,
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
    saving_throws: Sequence[modifier.Modifier] = [modifier.Modifier.CHARISMA],
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
    primary_modifiers: Sequence[modifier.Modifier] = [modifier.Modifier.CHARISMA],
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


def subclass_factory(
    subclass_id: UUID = uuid4(),
    class_id: UUID = uuid4(),
    name: str = "subclass_name",
    description: str = "subclass_description",
    name_in_english: str = "subclass_name_in_english",
):
    return character_subclass.CharacterSubclass(
        subclass_id=subclass_id,
        class_id=class_id,
        name=name,
        description=description,
        name_in_english=name_in_english,
    )


def class_feature_factory(
    feature_id: UUID = uuid4(),
    class_id: UUID = uuid4(),
    name: str = "class_feature_name",
    description: str = "class_feature_description",
    level: int = 1,
    name_in_english: str = "class_feature_name_in_english",
):
    return class_feature.ClassFeature(
        feature_id=feature_id,
        class_id=class_id,
        name=name,
        description=description,
        level=level,
        name_in_english=name_in_english,
    )


def class_level_dice_factory(
    dice: dice.Dice = dice_factory(), dice_description: str = "level_dice_description"
):
    return class_level.ClassLevelDice(dice=dice, dice_description=dice_description)


def class_level_spell_slots_factory(spell_slots: Sequence[int] = [0, 0, 0, 0, 0]):
    return class_level.ClassLevelSpellSlots(spell_slots=spell_slots)


def class_level_points_factory(
    points: int = 1, description: str = "class_level_points_description"
):
    return class_level.ClassLevelPoints(points=points, description=description)


def class_level_bonus_damage_factory(
    damage: int = 1, description: str = "class_level_bonus_damage_description"
):
    return class_level.ClassLevelBonusDamage(damage=damage, description=description)


def class_level_increase_speed_factory(
    speed: length.Length = length_factory(),
    description: str = "class_level_increase_speed_description",
):
    return class_level.ClassLevelIncreaseSpeed(speed=speed, description=description)


def class_level_factory(
    level_id: UUID = uuid4(),
    class_id: UUID = uuid4(),
    level: int = 1,
    dice: class_level.ClassLevelDice | None = None,
    spell_slots: class_level.ClassLevelSpellSlots | None = None,
    number_cantrips_know: int | None = None,
    number_spells_know: int | None = None,
    number_arcanums_know: int | None = None,
    points: class_level.ClassLevelPoints | None = None,
    bonus_damage: class_level.ClassLevelBonusDamage | None = None,
    increase_speed: class_level.ClassLevelIncreaseSpeed | None = None,
):
    return class_level.ClassLevel(
        level_id=level_id,
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


def feat_required_modifier_factory(
    modifier: modifier.Modifier = modifier.Modifier.DEXTERITY, min_value: int = 10
):
    return feat.FeatRequiredModifier(modifier=modifier, min_value=min_value)


def feat_factory(
    feat_id: UUID = uuid4(),
    name: str = "feat_name",
    description: str = "feat_description",
    caster: bool = False,
    required_modifiers: Sequence[feat.FeatRequiredModifier] = [],
    required_armor_types: Sequence[armor.ArmorType] = [],
    increase_modifiers: Sequence[modifier.Modifier] = [],
):
    return feat.Feat(
        feat_id=feat_id,
        name=name,
        description=description,
        caster=caster,
        required_modifiers=required_modifiers,
        required_armor_types=required_armor_types,
        increase_modifiers=increase_modifiers,
    )


def material_factory(
    material_id: UUID = uuid4(),
    name: str = "material_name",
    description: str = "material_description",
):
    return material.Material(
        material_id=material_id, name=name, description=description
    )


def material_component_factory(
    material_id: UUID = uuid4(),
    name: str = "material_component_name",
    description: str = "material_component_description",
):
    return material_component.MaterialComponent(
        material_id=material_id, name=name, description=description
    )


def race_speed_factory(
    base_speed: length.Length = length_factory(),
    description: str = "race_speed_description",
):
    return race.RaceSpeed(base_speed=base_speed, description=description)


def race_age_factory(max_age: int = 50, description: str = "race_age_description"):
    return race.RaceAge(max_age=max_age, description=description)


def race_increase_modifier_factory(
    modifier: modifier.Modifier = modifier.Modifier.CONSTITUTION, bonus: int = 5
):
    return race.RaceIncreaseModifier(modifier=modifier, bonus=bonus)


def race_feature_factory(
    name: str = "race_feature_name", description: str = "race_feature_description"
):
    return race.RaceFeature(name=name, description=description)


def race_factory(
    race_id: UUID = uuid4(),
    name: str = "race_name",
    description: str = "race_description",
    creature_type: creature_type.CreatureType = creature_type.CreatureType.ABERRATION,
    creature_size: creature_size.CreatureSize = creature_size.CreatureSize.HUGE,
    speed: race.RaceSpeed = race_speed_factory(),
    age: race.RaceAge = race_age_factory(),
    increase_modifiers: Sequence[race.RaceIncreaseModifier] = [],
    features: Sequence[race.RaceFeature] = [],
    name_in_english: str = "race_name_in_english",
    source_id: UUID = uuid4(),
):
    return race.Race(
        race_id=race_id,
        name=name,
        description=description,
        creature_type=creature_type,
        creature_size=creature_size,
        speed=speed,
        age=age,
        increase_modifiers=increase_modifiers,
        features=features,
        name_in_english=name_in_english,
        source_id=source_id,
    )


def source_factory(
    source_id: UUID = uuid4(),
    name: str = "source_name",
    description: str = "source_description",
    name_in_english: str = "source_name_in_english",
):
    return source.Source(
        source_id=source_id,
        name=name,
        description=description,
        name_in_english=name_in_english,
    )


def spell_components_factory(
    verbal: bool = False,
    symbolic: bool = False,
    material: bool = False,
    materials: Sequence[UUID] = [],
):
    return spell.SpellComponents(
        verbal=verbal, symbolic=symbolic, material=material, materials=materials
    )


def spell_factory(
    spell_id: UUID = uuid4(),
    class_ids: Sequence[UUID] = [],
    subclass_ids: Sequence[UUID] = [],
    name: str = "spell_name",
    description: str = "spell_description",
    next_level_description: str = "spell_next_level_description",
    level: int = 1,
    school: spell.SpellSchool = spell.SpellSchool.ABJURATION,
    damage_type: damage_type.DamageType | None = None,
    duration: game_time.GameTime | None = None,
    casting_time: game_time.GameTime = game_time_factory(),
    spell_range: length.Length = length_factory(),
    splash: length.Length | None = None,
    components: spell.SpellComponents = spell_components_factory(),
    concentration: bool = False,
    ritual: bool = False,
    saving_throws: Sequence[modifier.Modifier] = [],
    name_in_english: str = "spell_name_in_english",
    source_id: UUID = uuid4(),
):
    return spell.Spell(
        spell_id=spell_id,
        class_ids=class_ids,
        subclass_ids=subclass_ids,
        name=name,
        description=description,
        next_level_description=next_level_description,
        level=level,
        school=school,
        damage_type=damage_type,
        duration=duration,
        casting_time=casting_time,
        spell_range=spell_range,
        splash=splash,
        components=components,
        concentration=concentration,
        ritual=ritual,
        saving_throws=saving_throws,
        name_in_english=name_in_english,
        source_id=source_id,
    )


def subclass_feature_factory(
    feature_id: UUID = uuid4(),
    subclass_id: UUID = uuid4(),
    name: str = "subclass_feature_name",
    description: str = "subclass_feature_description",
    level: int = 1,
    name_in_english: str = "subclass_feature_name_in_english",
):
    return subclass_feature.SubclassFeature(
        feature_id=feature_id,
        subclass_id=subclass_id,
        name=name,
        description=description,
        level=level,
        name_in_english=name_in_english,
    )


def subrace_factory(
    subrace_id: UUID = uuid4(),
    race_id: UUID = uuid4(),
    name: str = "subrace_name",
    description: str = "subrace_description",
    increase_modifiers: Sequence[subrace.SubraceIncreaseModifier] = [],
    features: Sequence[subrace.SubraceFeature] = [],
    name_in_english: str = "subrace_name_in_english",
):
    return subrace.Subrace(
        subrace_id=subrace_id,
        race_id=race_id,
        name=name,
        description=description,
        increase_modifiers=increase_modifiers,
        features=features,
        name_in_english=name_in_english,
    )


def tool_utilize_factory(action: str = "tool_utilize_action", complexity: int = 10):
    return tool.ToolUtilize(action=action, complexity=complexity)


def tool_factory(
    tool_id: UUID = uuid4(),
    tool_type: tool.ToolType = tool.ToolType.ARTISANS_TOOLS,
    name: str = "tool_name",
    description: str = "tool_description",
    cost: coin.Coins = coin_factory(),
    weight: weight.Weight = weight_factory(),
    utilizes: Sequence[tool.ToolUtilize] = [],
):
    return tool.Tool(
        tool_id=tool_id,
        tool_type=tool_type,
        name=name,
        description=description,
        cost=cost,
        weight=weight,
        utilizes=utilizes,
    )


def weapon_kind_factory(
    weapon_kind_id: UUID = uuid4(),
    name: str = "weapon_kind_name",
    description: str = "weapon_kind_description",
    weapon_type: weapon_kind.WeaponType = weapon_kind.WeaponType.MARTIAL_MELEE,
):
    return weapon_kind.WeaponKind(
        weapon_kind_id=weapon_kind_id,
        name=name,
        description=description,
        weapon_type=weapon_type,
    )


def weapon_property_factory(
    weapon_property_id: UUID = uuid4(),
    name: weapon_property.WeaponPropertyName = weapon_property.WeaponPropertyName.HEAVY,
    description: str = "weapon_property_description",
    base_range: length.Length | None = None,
    max_range: length.Length | None = None,
    second_hand_dice: dice.Dice | None = None,
):
    return weapon_property.WeaponProperty(
        weapon_property_id=weapon_property_id,
        name=name,
        description=description,
        base_range=base_range,
        max_range=max_range,
        second_hand_dice=second_hand_dice,
    )


def weapon_damage_factory(
    dice: dice.Dice = dice_factory(),
    damage_type: damage_type.DamageType = damage_type.DamageType.ACID,
    bonus_damage: int = 1,
):
    return weapon.WeaponDamage(
        dice=dice, damage_type=damage_type, bonus_damage=bonus_damage
    )


def weapon_factory(
    weapon_id: UUID = uuid4(),
    weapon_kind_id: UUID = uuid4(),
    name: str = "weapon_name",
    description: str = "weapon_description",
    cost: coin.Coins = coin_factory(),
    damage: weapon.WeaponDamage = weapon_damage_factory(),
    weight: weight.Weight = weight_factory(),
    weapon_property_ids: Sequence[UUID] = [],
    material_id: UUID = uuid4(),
):
    return weapon.Weapon(
        weapon_id=weapon_id,
        weapon_kind_id=weapon_kind_id,
        name=name,
        description=description,
        cost=cost,
        damage=damage,
        weight=weight,
        weapon_property_ids=weapon_property_ids,
        material_id=material_id,
    )
