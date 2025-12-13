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
from domain.creature_size import CreatureSize
from domain.creature_type import CreatureType
from domain.damage_type import DamageType
from domain.dice import DiceType
from domain.game_time import GameTimeUnit
from domain.length import LengthUnit
from domain.modifier import Modifier
from domain.skill import Skill
from domain.spell.school import SpellSchool
from domain.tool.tool_type import ToolType
from domain.weapon_kind.weapon_type import WeaponType
from domain.weight import WeightUnit


def game_time_model_factory(
    count: int = 10, unit: str = GameTimeUnit.ACTION.name.lower()
) -> game_time.AppGameTime:
    return game_time.AppGameTime(count=count, unit=unit)


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
    class_level_id: UUID = uuid4(),
    class_id: UUID = uuid4(),
    level: int = 1,
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


def feat_required_modifier_model_factory(
    modifier: str = Modifier.STRENGTH.name.lower(), min_value: int = 16
) -> feat.AppFeatRequiredModifier:
    return feat.AppFeatRequiredModifier(modifier=modifier, min_value=min_value)


def feat_model_factory(
    feat_id: UUID = uuid4(),
    name: str = "feat_name",
    description: str = "feat_description",
    caster: bool = False,
    required_armor_types: Sequence[str] = [ArmorType.HEAVY_ARMOR.name.lower()],
    required_modifiers: Sequence[feat.AppFeatRequiredModifier] = [
        feat_required_modifier_model_factory()
    ],
    increase_modifiers: Sequence[str] = [Modifier.CHARISMA.name.lower()],
) -> feat.AppFeat:
    return feat.AppFeat(
        feat_id=feat_id,
        name=name,
        description=description,
        caster=caster,
        required_armor_types=required_armor_types,
        required_modifiers=required_modifiers,
        increase_modifiers=increase_modifiers,
    )


def material_model_factory(
    material_id: UUID = uuid4(),
    name: str = "material_name",
    description: str = "material_description",
) -> material.AppMaterial:
    return material.AppMaterial(
        material_id=material_id, name=name, description=description
    )


def material_component_model_factory(
    material_id: UUID = uuid4(),
    name: str = "material_component_name",
    description: str = "material_component_description",
) -> material_component.AppMaterialComponent:
    return material_component.AppMaterialComponent(
        material_id=material_id, name=name, description=description
    )


def race_age_model_factory(
    max_age: int = 100, description: str = "race_age_description"
) -> race.AppRaceAge:
    return race.AppRaceAge(max_age=max_age, description=description)


def race_speed_model_factory(
    base_speed: length.AppLength = length_model_factory(),
    description: str = "race_speed_description",
) -> race.AppRaceSpeed:
    return race.AppRaceSpeed(base_speed=base_speed, description=description)


def race_feature_model_factory(
    name: str = "race_feature_name", description: str = "race_feature_description"
) -> race.AppRaceFeature:
    return race.AppRaceFeature(name=name, description=description)


def race_increase_modifier_model_factory(
    modifier: str = Modifier.CHARISMA.name.lower(), bonus: int = 2
) -> race.AppRaceIncreaseModifier:
    return race.AppRaceIncreaseModifier(modifier=modifier, bonus=bonus)


def race_model_factory(
    race_id: UUID = uuid4(),
    name: str = "race_name",
    description: str = "race_description",
    creature_type: str = CreatureType.ABERRATION.name.lower(),
    creature_size: str = CreatureSize.MEDIUM.name.lower(),
    speed: race.AppRaceSpeed = race_speed_model_factory(),
    age: race.AppRaceAge = race_age_model_factory(),
    increase_modifiers: Sequence[race.AppRaceIncreaseModifier] = [
        race_increase_modifier_model_factory()
    ],
    source_id: UUID = uuid4(),
    features: Sequence[race.AppRaceFeature] = [race_feature_model_factory()],
    name_in_english: str = "race_name_in_english",
) -> race.AppRace:
    return race.AppRace(
        race_id=race_id,
        name=name,
        description=description,
        creature_type=creature_type,
        creature_size=creature_size,
        speed=speed,
        age=age,
        increase_modifiers=increase_modifiers,
        source_id=source_id,
        features=features,
        name_in_english=name_in_english,
    )


def source_model_factory(
    source_id: UUID = uuid4(),
    name: str = "source_name",
    description: str = "source_description",
    name_in_english: str = "source_name_in_english",
) -> source.AppSource:
    return source.AppSource(
        source_id=source_id,
        name=name,
        description=description,
        name_in_english=name_in_english,
    )


def spell_component_model_factory(
    verbal: bool = False,
    symbolic: bool = False,
    material: bool = False,
    materials: list[UUID] = [],
) -> spell.AppSpellComponents:
    return spell.AppSpellComponents(
        verbal=verbal, symbolic=symbolic, material=material, materials=materials
    )


def spell_model_factory(
    spell_id: UUID = uuid4(),
    class_ids: Sequence[UUID] = [],
    subclass_ids: Sequence[UUID] = [],
    name: str = "spell_name",
    description: str = "spell_description",
    next_level_description: str = "spell_next_level_description",
    level: int = 1,
    school: str = SpellSchool.ABJURATION.name.lower(),
    damage_type: str | None = None,
    duration: game_time.AppGameTime | None = None,
    casting_time: game_time.AppGameTime = game_time_model_factory(),
    spell_range: length.AppLength = length_model_factory(),
    splash: length.AppLength | None = None,
    components: spell.AppSpellComponents = spell_component_model_factory(),
    concentration: bool = False,
    ritual: bool = False,
    saving_throws: Sequence[str] = [],
    name_in_english: str = "spell_name_in_english",
    source_id: UUID = uuid4(),
) -> spell.AppSpell:
    return spell.AppSpell(
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


def subclass_feature_model_factory(
    feature_id: UUID = uuid4(),
    subclass_id: UUID = uuid4(),
    name: str = "subclass_feature_name",
    description: str = "subclass_feature_description",
    level: int = 1,
    name_in_english: str = "subclass_feature_name_in_english",
) -> subclass_feature.AppSubclassFeature:
    return subclass_feature.AppSubclassFeature(
        feature_id=feature_id,
        subclass_id=subclass_id,
        name=name,
        description=description,
        level=level,
        name_in_english=name_in_english,
    )


def subrace_feature_model_factory(
    name: str = "subrace_feature_name", description: str = "subrace_feature_description"
) -> subrace.AppSubraceFeature:
    return subrace.AppSubraceFeature(name=name, description=description)


def subrace_increase_modifier_model_factory(
    modifier: str = Modifier.CHARISMA.name.lower(), bonus: int = 2
) -> subrace.AppSubraceIncreaseModifier:
    return subrace.AppSubraceIncreaseModifier(modifier=modifier, bonus=bonus)


def subrace_model_factory(
    subrace_id: UUID = uuid4(),
    race_id: UUID = uuid4(),
    name: str = "subrace_name",
    description: str = "subrace_description",
    increase_modifiers: Sequence[subrace.AppSubraceIncreaseModifier] = [
        subrace_increase_modifier_model_factory()
    ],
    name_in_english: str = "subrace_name_in_english",
    features: Sequence[subrace.AppSubraceFeature] = [subrace_feature_model_factory()],
) -> subrace.AppSubrace:
    return subrace.AppSubrace(
        subrace_id=subrace_id,
        race_id=race_id,
        name=name,
        description=description,
        increase_modifiers=increase_modifiers,
        name_in_english=name_in_english,
        features=features,
    )


def tool_utilizes_model_factory(
    action: str = "action_name", complexity: int = 15
) -> tool.AppToolUtilizes:
    return tool.AppToolUtilizes(action=action, complexity=complexity)


def tool_model_factory(
    tool_id: UUID = uuid4(),
    tool_type: str = ToolType.ARTISANS_TOOLS.name.lower(),
    name: str = "tool_name",
    description: str = "tool_description",
    cost: coin.AppCoins = coins_model_factory(),
    weight: weight.AppWeight = weight_model_factory(),
    utilizes: Sequence[tool.AppToolUtilizes] = [tool_utilizes_model_factory()],
) -> tool.AppTool:
    return tool.AppTool(
        tool_id=tool_id,
        tool_type=tool_type,
        name=name,
        description=description,
        cost=cost,
        weight=weight,
        utilizes=utilizes,
    )


def weapon_damage_model_factory(
    dice: dice.AppDice = dice_model_factory(),
    damage_type: str = DamageType.ACID.name.lower(),
    bonus_damage: int = 2,
) -> weapon.AppWeaponDamage:
    return weapon.AppWeaponDamage(
        dice=dice, damage_type=damage_type, bonus_damage=bonus_damage
    )


def weapon_model_factory(
    weapon_id: UUID = uuid4(),
    weapon_kind_id: UUID = uuid4(),
    name: str = "weapon_name",
    description: str = "weapon_description",
    cost: coin.AppCoins = coins_model_factory(),
    damage: weapon.AppWeaponDamage = weapon_damage_model_factory(),
    weight: weight.AppWeight = weight_model_factory(),
    weapon_property_ids: Sequence[UUID] = [uuid4()],
    material_id: UUID = uuid4(),
) -> weapon.AppWeapon:
    return weapon.AppWeapon(
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


def weapon_kind_model_factory(
    weapon_kind_id: UUID = uuid4(),
    weapon_type: str = WeaponType.MARTIAL_MELEE.name.lower(),
    name: str = "weapon_kind_name",
    description: str = "weapon_kind_description",
) -> weapon_kind.AppWeaponKind:
    return weapon_kind.AppWeaponKind(
        weapon_kind_id=weapon_kind_id,
        weapon_type=weapon_type,
        name=name,
        description=description,
    )


def weapon_property_model_factory(
    weapon_property_id: UUID = uuid4(),
    name: str = "weapon_property_name",
    description: str = "weapon_property_description",
    base_range: length.AppLength | None = None,
    max_range: length.AppLength | None = None,
    second_hand_dice: dice.AppDice | None = None,
) -> weapon_property.AppWeaponProperty:
    return weapon_property.AppWeaponProperty(
        weapon_property_id=weapon_property_id,
        name=name,
        description=description,
        base_range=base_range,
        max_range=max_range,
        second_hand_dice=second_hand_dice,
    )


def user_model_factory(user_id: UUID = uuid4()) -> user.AppUser:
    return user.AppUser(user_id=user_id)
