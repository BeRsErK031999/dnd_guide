from typing import Sequence
from uuid import UUID, uuid4

from application.dto.command import (
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
    weapon,
    weapon_kind,
    weapon_property,
    weight,
)
from domain.armor.armor_type import ArmorType
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
from domain.weapon_property.name import WeaponPropertyName
from domain.weight import WeightUnit


def game_time_command_factory(
    count: int = 1, unit: str = GameTimeUnit.ACTION.name.lower()
) -> game_time.GameTimeCommand:
    return game_time.GameTimeCommand(count=count, unit=unit)


def coin_command_factory(
    count: int = 10, piece_type: str = PieceType.COPPER.name.lower()
) -> coin.CoinCommand:
    return coin.CoinCommand(count=count, piece_type=piece_type)


def dice_command_factory(
    count: int = 10, dice_type: str = DiceType.D10.name.lower()
) -> dice.DiceCommand:
    return dice.DiceCommand(count=count, dice_type=dice_type)


def length_command_factory(
    count: float = 30, unit: str = LengthUnit.FT.name.lower()
) -> length.LengthCommand:
    return length.LengthCommand(count=count, unit=unit)


def weight_command_factory(
    count: float = 10, unit: str = WeightUnit.LB.name.lower()
) -> weight.WeightCommand:
    return weight.WeightCommand(count=count, unit=unit)


def armor_class_command(
    base_class: int = 10,
    modifier: str | None = None,
    max_modifier_bonus: int | None = None,
) -> armor.ArmorClassCommand:
    return armor.ArmorClassCommand(
        base_class=base_class,
        modifier=modifier,
        max_modifier_bonus=max_modifier_bonus,
    )


class ArmorCommandFactory:
    @staticmethod
    def create(
        armor_class: armor.ArmorClassCommand = armor_class_command(),
        armor_weight: weight.WeightCommand = weight_command_factory(),
        armor_cost: coin.CoinCommand = coin_command_factory(),
        user_id: UUID = uuid4(),
        armor_type: str = ArmorType.MEDIUM_ARMOR.name.lower(),
        name: str = "armor_name",
        description: str = "armor_description",
        strength: int = 15,
        stealth: bool = True,
        material_id: UUID = uuid4(),
    ) -> armor.CreateArmorCommand:
        return armor.CreateArmorCommand(
            user_id=user_id,
            armor_type=armor_type,
            name=name,
            description=description,
            strength=strength,
            stealth=stealth,
            armor_class=armor_class,
            weight=armor_weight,
            cost=armor_cost,
            material_id=material_id,
        )

    @staticmethod
    def update(
        armor_class: armor.ArmorClassCommand | None = None,
        armor_weight: weight.WeightCommand | None = None,
        cost: coin.CoinCommand | None = None,
        user_id: UUID = uuid4(),
        armor_id: UUID = uuid4(),
        armor_type: str | None = None,
        name: str | None = None,
        description: str | None = None,
        strength: int | None = None,
        stealth: bool | None = None,
        material_id: UUID | None = None,
    ) -> armor.UpdateArmorCommand:
        return armor.UpdateArmorCommand(
            user_id=user_id,
            armor_id=armor_id,
            armor_type=armor_type,
            name=name,
            description=description,
            strength=strength,
            stealth=stealth,
            armor_class=armor_class,
            weight=armor_weight,
            cost=cost,
            material_id=material_id,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), armor_id: UUID = uuid4()
    ) -> armor.DeleteArmorCommand:
        return armor.DeleteArmorCommand(user_id=user_id, armor_id=armor_id)


def class_hits_command_factory(
    hit_dice: dice.DiceCommand = dice_command_factory(),
    starting_hits: int = 10,
    hit_modifier: str = Modifier.CONSTITUTION.name.lower(),
    next_level_hits: int = 5,
) -> character_class.ClassHitsCommand:
    return character_class.ClassHitsCommand(
        hit_dice=hit_dice,
        starting_hits=starting_hits,
        hit_modifier=hit_modifier,
        next_level_hits=next_level_hits,
    )


def class_proficiencies_command_factory(
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
) -> character_class.ClassProficienciesCommand:
    return character_class.ClassProficienciesCommand(
        armors=armors,
        weapons=weapons,
        tools=tools,
        saving_throws=saving_throws,
        skills=skills,
        number_skills=number_skills,
        number_tools=number_tools,
    )


class ClassCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        name: str = "class_name",
        description: str = "class_description",
        primary_modifiers: Sequence[str] = [
            Modifier.STRENGTH.name.lower(),
            Modifier.CONSTITUTION.name.lower(),
        ],
        hits: character_class.ClassHitsCommand = class_hits_command_factory(),
        proficiencies: character_class.ClassProficienciesCommand = class_proficiencies_command_factory(),
        name_in_english: str = "class_name_english",
        source_id: UUID = uuid4(),
    ) -> character_class.CreateClassCommand:
        return character_class.CreateClassCommand(
            user_id=user_id,
            name=name,
            description=description,
            primary_modifiers=primary_modifiers,
            hits=hits,
            proficiencies=proficiencies,
            name_in_english=name_in_english,
            source_id=source_id,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        class_id: UUID = uuid4(),
        name: str | None = None,
        description: str | None = None,
        primary_modifiers: Sequence[str] | None = None,
        hits: character_class.ClassHitsCommand | None = None,
        proficiencies: character_class.ClassProficienciesCommand | None = None,
        name_in_english: str | None = None,
        source_id: UUID | None = None,
    ) -> character_class.UpdateClassCommand:
        return character_class.UpdateClassCommand(
            user_id=user_id,
            class_id=class_id,
            name=name,
            description=description,
            primary_modifiers=primary_modifiers,
            hits=hits,
            proficiencies=proficiencies,
            name_in_english=name_in_english,
            source_id=source_id,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), class_id: UUID = uuid4()
    ) -> character_class.DeleteClassCommand:
        return character_class.DeleteClassCommand(user_id=user_id, class_id=class_id)


class SubclassCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        class_id: UUID = uuid4(),
        name: str = "subclass_name",
        description: str = "subclass_description",
        name_in_english: str = "subclass_name_english",
    ) -> character_subclass.CreateSubclassCommand:
        return character_subclass.CreateSubclassCommand(
            user_id=user_id,
            class_id=class_id,
            name=name,
            description=description,
            name_in_english=name_in_english,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        subclass_id: UUID = uuid4(),
        class_id: UUID | None = None,
        name: str | None = None,
        description: str | None = None,
        name_in_english: str | None = None,
    ) -> character_subclass.UpdateSubclassCommand:
        return character_subclass.UpdateSubclassCommand(
            user_id=user_id,
            subclass_id=subclass_id,
            class_id=class_id,
            name=name,
            description=description,
            name_in_english=name_in_english,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), subclass_id: UUID = uuid4()
    ) -> character_subclass.DeleteSubclassCommand:
        return character_subclass.DeleteSubclassCommand(
            user_id=user_id, subclass_id=subclass_id
        )


class ClassFeatureCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        class_id: UUID = uuid4(),
        name: str = "feature_name",
        description: str = "feature_description",
        level: int = 1,
        name_in_english: str = "feature_name_english",
    ) -> class_feature.CreateClassFeatureCommand:
        return class_feature.CreateClassFeatureCommand(
            user_id=user_id,
            class_id=class_id,
            name=name,
            description=description,
            level=level,
            name_in_english=name_in_english,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        feature_id: UUID = uuid4(),
        class_id: UUID | None = None,
        name: str | None = None,
        description: str | None = None,
        level: int | None = None,
        name_in_english: str | None = None,
    ) -> class_feature.UpdateClassFeatureCommand:
        return class_feature.UpdateClassFeatureCommand(
            user_id=user_id,
            feature_id=feature_id,
            class_id=class_id,
            name=name,
            description=description,
            level=level,
            name_in_english=name_in_english,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), feature_id: UUID = uuid4()
    ) -> class_feature.DeleteClassFeatureCommand:
        return class_feature.DeleteClassFeatureCommand(
            user_id=user_id, feature_id=feature_id
        )


def class_level_dice_command_factory(
    hit_dice: dice.DiceCommand = dice_command_factory(),
    description: str = "class_level_dice_description",
) -> class_level.ClassLevelDiceCommand:
    return class_level.ClassLevelDiceCommand(dice=hit_dice, description=description)


def class_level_points_command_factory(
    points: int = 2, description: str = "class_level_points_description"
) -> class_level.ClassLevelPointsCommand:
    return class_level.ClassLevelPointsCommand(points=points, description=description)


def class_level_bonus_damage_command_factory(
    damage: int = 1,
    description: str = "class_level_bonus_damage_description",
) -> class_level.ClassLevelBonusDamageCommand:
    return class_level.ClassLevelBonusDamageCommand(
        damage=damage, description=description
    )


def class_level_increase_speed_command_factory(
    speed: length.LengthCommand = length_command_factory(),
    description: str = "class_level_increase_speed_description",
) -> class_level.ClassLevelIncreaseSpeedCommand:
    return class_level.ClassLevelIncreaseSpeedCommand(
        speed=speed, description=description
    )


class ClassLevelCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        class_id: UUID = uuid4(),
        level: int = 1,
        dice: class_level.ClassLevelDiceCommand | None = None,
        spell_slots: Sequence[int] | None = None,
        number_cantrips_know: int | None = None,
        number_spells_know: int | None = None,
        number_arcanums_know: int | None = None,
        points: class_level.ClassLevelPointsCommand | None = None,
        bonus_damage: class_level.ClassLevelBonusDamageCommand | None = None,
        increase_speed: class_level.ClassLevelIncreaseSpeedCommand | None = None,
    ) -> class_level.CreateClassLevelCommand:
        return class_level.CreateClassLevelCommand(
            user_id=user_id,
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

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        class_level_id: UUID = uuid4(),
        class_id: UUID | None = None,
        level: int | None = None,
        dice: class_level.ClassLevelDiceCommand | None = None,
        spell_slots: Sequence[int] | None = None,
        number_cantrips_know: int | None = None,
        number_spells_know: int | None = None,
        number_arcanums_know: int | None = None,
        points: class_level.ClassLevelPointsCommand | None = None,
        bonus_damage: class_level.ClassLevelBonusDamageCommand | None = None,
        increase_speed: class_level.ClassLevelIncreaseSpeedCommand | None = None,
    ) -> class_level.UpdateClassLevelCommand:
        return class_level.UpdateClassLevelCommand(
            user_id=user_id,
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

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), class_level_id: UUID = uuid4()
    ) -> class_level.DeleteClassLevelCommand:
        return class_level.DeleteClassLevelCommand(
            user_id=user_id, class_level_id=class_level_id
        )


def feat_required_modifier_command_factory(
    modifier: str = Modifier.STRENGTH.name.lower(), min_value: int = 16
) -> feat.FeatRequiredModifierCommand:
    return feat.FeatRequiredModifierCommand(modifier=modifier, min_value=min_value)


class FeatCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        name: str = "feat_name",
        description: str = "feat_description",
        caster: bool = False,
        required_armor_types: Sequence[str] = [ArmorType.HEAVY_ARMOR.name.lower()],
        required_modifiers: Sequence[feat.FeatRequiredModifierCommand] = [
            feat_required_modifier_command_factory()
        ],
        increase_modifiers: Sequence[str] = [Modifier.CHARISMA.name.lower()],
    ) -> feat.CreateFeatCommand:
        return feat.CreateFeatCommand(
            user_id=user_id,
            name=name,
            description=description,
            caster=caster,
            required_armor_types=required_armor_types,
            required_modifiers=required_modifiers,
            increase_modifiers=increase_modifiers,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        feat_id: UUID = uuid4(),
        name: str | None = None,
        description: str | None = None,
        caster: bool | None = None,
        required_armor_types: Sequence[str] | None = None,
        required_modifiers: Sequence[feat.FeatRequiredModifierCommand] | None = None,
        increase_modifiers: Sequence[str] | None = None,
    ) -> feat.UpdateFeatCommand:
        return feat.UpdateFeatCommand(
            user_id=user_id,
            feat_id=feat_id,
            name=name,
            description=description,
            caster=caster,
            required_armor_types=required_armor_types,
            required_modifiers=required_modifiers,
            increase_modifiers=increase_modifiers,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), feat_id: UUID = uuid4()
    ) -> feat.DeleteFeatCommand:
        return feat.DeleteFeatCommand(user_id=user_id, feat_id=feat_id)


class MaterialCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        name: str = "material_name",
        description: str = "material_description",
    ) -> material.CreateMaterialCommand:
        return material.CreateMaterialCommand(
            user_id=user_id, name=name, description=description
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        material_id: UUID = uuid4(),
        name: str | None = None,
        description: str | None = None,
    ) -> material.UpdateMaterialCommand:
        return material.UpdateMaterialCommand(
            user_id=user_id, material_id=material_id, name=name, description=description
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), material_id: UUID = uuid4()
    ) -> material.DeleteMaterialCommand:
        return material.DeleteMaterialCommand(user_id=user_id, material_id=material_id)


class MaterialComponentCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        name: str = "material_component_name",
        description: str = "material_component_description",
    ) -> material_component.CreateMaterialComponentCommand:
        return material_component.CreateMaterialComponentCommand(
            user_id=user_id, name=name, description=description
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        material_id: UUID = uuid4(),
        name: str | None = None,
        description: str | None = None,
    ) -> material_component.UpdateMaterialComponentCommand:
        return material_component.UpdateMaterialComponentCommand(
            user_id=user_id, material_id=material_id, name=name, description=description
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), material_id: UUID = uuid4()
    ) -> material_component.DeleteMaterialComponentCommand:
        return material_component.DeleteMaterialComponentCommand(
            user_id=user_id, material_id=material_id
        )


def race_feature_command_factory(
    name: str = "race_feature_name", description: str = "race_feature_description"
) -> race.RaceFeatureCommand:
    return race.RaceFeatureCommand(name=name, description=description)


def race_age_command_factory(
    max_age: int = 100, description: str = "race_age_description"
) -> race.RaceAgeCommand:
    return race.RaceAgeCommand(max_age=max_age, description=description)


def race_speed_command_factory(
    base_speed: length.LengthCommand = length_command_factory(),
    description: str = "race_speed_description",
) -> race.RaceSpeedCommand:
    return race.RaceSpeedCommand(base_speed=base_speed, description=description)


def race_increase_modifier_command_factory(
    modifier: str = Modifier.CHARISMA.name.lower(), bonus: int = 2
) -> race.RaceIncreaseModifierCommand:
    return race.RaceIncreaseModifierCommand(modifier=modifier, bonus=bonus)


class RaceCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        name: str = "race_name",
        description: str = "race_description",
        creature_type: str = CreatureType.DRAGON.name.lower(),
        creature_size: str = CreatureSize.MEDIUM.name.lower(),
        speed: race.RaceSpeedCommand = race_speed_command_factory(),
        age: race.RaceAgeCommand = race_age_command_factory(),
        increase_modifiers: Sequence[race.RaceIncreaseModifierCommand] = [
            race_increase_modifier_command_factory()
        ],
        source_id: UUID = uuid4(),
        features: Sequence[race.RaceFeatureCommand] = [race_feature_command_factory()],
        name_in_english: str = "race_name_in_english",
    ) -> race.CreateRaceCommand:
        return race.CreateRaceCommand(
            user_id=user_id,
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

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        race_id: UUID = uuid4(),
        name: str | None = None,
        description: str | None = None,
        creature_size: str | None = None,
        creature_type: str | None = None,
        speed: race.RaceSpeedCommand | None = None,
        age: race.RaceAgeCommand | None = None,
        increase_modifiers: Sequence[race.RaceIncreaseModifierCommand] | None = None,
        new_features: Sequence[race.RaceFeatureCommand] | None = None,
        add_features: Sequence[race.RaceFeatureCommand] | None = None,
        remove_features: Sequence[str] | None = None,
        name_in_english: str | None = None,
        source_id: UUID | None = None,
    ) -> race.UpdateRaceCommand:
        return race.UpdateRaceCommand(
            user_id=user_id,
            race_id=race_id,
            name=name,
            description=description,
            creature_size=creature_size,
            creature_type=creature_type,
            speed=speed,
            age=age,
            increase_modifiers=increase_modifiers,
            new_features=new_features,
            add_features=add_features,
            remove_features=remove_features,
            name_in_english=name_in_english,
            source_id=source_id,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), race_id: UUID = uuid4()
    ) -> race.DeleteRaceCommand:
        return race.DeleteRaceCommand(user_id=user_id, race_id=race_id)


class SourceCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        name: str = "source_name",
        description: str = "source_description",
        name_in_english: str = "source_name_in_english",
    ) -> source.CreateSourceCommand:
        return source.CreateSourceCommand(
            user_id=user_id,
            name=name,
            description=description,
            name_in_english=name_in_english,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        source_id: UUID = uuid4(),
        name: str | None = None,
        description: str | None = None,
        name_in_english: str | None = None,
    ) -> source.UpdateSourceCommand:
        return source.UpdateSourceCommand(
            user_id=user_id,
            source_id=source_id,
            name=name,
            description=description,
            name_in_english=name_in_english,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), source_id: UUID = uuid4()
    ) -> source.DeleteSourceCommand:
        return source.DeleteSourceCommand(user_id=user_id, source_id=source_id)


def spell_damage_type_command_factory(
    name: str | None = None,
) -> spell.SpellDamageTypeCommand:
    return spell.SpellDamageTypeCommand(name=name)


def spell_duration_command_factory(
    game_time_c: game_time.GameTimeCommand | None = None,
) -> spell.SpellDurationCommand:
    return spell.SpellDurationCommand(game_time=game_time_c)


def splash_command_factory(
    splash: length.LengthCommand | None = None,
) -> spell.SplashCommand:
    return spell.SplashCommand(splash=splash)


def spell_components_command_factory(
    verbal: bool = False,
    symbolic: bool = False,
    material: bool = False,
    materials: list[UUID] = [],
) -> spell.SpellComponentsCommand:
    return spell.SpellComponentsCommand(
        verbal=verbal, symbolic=symbolic, material=material, materials=materials
    )


class SpellCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        class_ids: Sequence[UUID] = [],
        subclass_ids: Sequence[UUID] = [],
        name: str = "spell_name",
        description: str = "spell_description",
        next_level_description: str = "spell_next_level_description",
        level: int = 1,
        school: str = SpellSchool.ABJURATION.name.lower(),
        damage_type: spell.SpellDamageTypeCommand = spell_damage_type_command_factory(),
        duration: spell.SpellDurationCommand = spell_duration_command_factory(),
        casting_time: game_time.GameTimeCommand = game_time_command_factory(),
        spell_range: length.LengthCommand = length_command_factory(),
        splash: spell.SplashCommand = splash_command_factory(),
        components: spell.SpellComponentsCommand = spell_components_command_factory(),
        concentration: bool = False,
        ritual: bool = False,
        saving_throws: Sequence[str] = [],
        name_in_english: str = "spell_name_in_english",
        source_id: UUID = uuid4(),
    ) -> spell.CreateSpellCommand:
        return spell.CreateSpellCommand(
            user_id=user_id,
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

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        spell_id: UUID = uuid4(),
        class_ids: Sequence[UUID] | None = None,
        subclass_ids: Sequence[UUID] | None = None,
        name: str | None = None,
        description: str | None = None,
        next_level_description: str | None = None,
        level: int | None = None,
        school: str | None = None,
        damage_type: spell.SpellDamageTypeCommand | None = None,
        duration: spell.SpellDurationCommand | None = None,
        casting_time: game_time.GameTimeCommand | None = None,
        spell_range: length.LengthCommand | None = None,
        splash: spell.SplashCommand | None = None,
        components: spell.SpellComponentsCommand | None = None,
        concentration: bool | None = None,
        ritual: bool | None = None,
        saving_throws: Sequence[str] | None = None,
        name_in_english: str | None = None,
        source_id: UUID | None = None,
    ) -> spell.UpdateSpellCommand:
        return spell.UpdateSpellCommand(
            user_id=user_id,
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

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), spell_id: UUID = uuid4()
    ) -> spell.DeleteSpellCommand:
        return spell.DeleteSpellCommand(user_id=user_id, spell_id=spell_id)


class SubclassFeatureCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        subclass_id: UUID = uuid4(),
        name: str = "subclass_feature_name",
        description: str = "subclass_feature_description",
        level: int = 1,
        name_in_english: str = "subclass_feature_name_in_english",
    ) -> subclass_feature.CreateSubclassFeatureCommand:
        return subclass_feature.CreateSubclassFeatureCommand(
            user_id=user_id,
            subclass_id=subclass_id,
            name=name,
            description=description,
            level=level,
            name_in_english=name_in_english,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        feature_id: UUID = uuid4(),
        subclass_id: UUID | None = None,
        name: str | None = None,
        description: str | None = None,
        level: int | None = None,
        name_in_english: str | None = None,
    ) -> subclass_feature.UpdateSubclassFeatureCommand:
        return subclass_feature.UpdateSubclassFeatureCommand(
            user_id=user_id,
            feature_id=feature_id,
            subclass_id=subclass_id,
            name=name,
            description=description,
            level=level,
            name_in_english=name_in_english,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), feature_id: UUID = uuid4()
    ) -> subclass_feature.DeleteSubclassFeatureCommand:
        return subclass_feature.DeleteSubclassFeatureCommand(
            user_id=user_id, feature_id=feature_id
        )


def subrace_feature_command_factory(
    name: str = "subrace_feature_name", description: str = "subrace_feature_description"
) -> subrace.SubraceFeatureCommand:
    return subrace.SubraceFeatureCommand(name=name, description=description)


def subrace_increase_modifier_command_factory(
    modifier: str = Modifier.CHARISMA.name.lower(), bonus: int = 2
) -> subrace.SubraceIncreaseModifierCommand:
    return subrace.SubraceIncreaseModifierCommand(modifier=modifier, bonus=bonus)


class SubraceCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        race_id: UUID = uuid4(),
        name: str = "subrace_name",
        description: str = "subrace_description",
        increase_modifiers: Sequence[subrace.SubraceIncreaseModifierCommand] = [
            subrace_increase_modifier_command_factory()
        ],
        name_in_english: str = "subrace_name_in_english",
        features: Sequence[subrace.SubraceFeatureCommand] = [
            subrace_feature_command_factory()
        ],
    ) -> subrace.CreateSubraceCommand:
        return subrace.CreateSubraceCommand(
            user_id=user_id,
            race_id=race_id,
            name=name,
            description=description,
            increase_modifiers=increase_modifiers,
            name_in_english=name_in_english,
            features=features,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        subrace_id: UUID = uuid4(),
        race_id: UUID | None = None,
        name: str | None = None,
        description: str | None = None,
        increase_modifiers: (
            Sequence[subrace.SubraceIncreaseModifierCommand] | None
        ) = None,
        new_features: Sequence[subrace.SubraceFeatureCommand] | None = None,
        add_features: Sequence[subrace.SubraceFeatureCommand] | None = None,
        remove_features: Sequence[str] | None = None,
        name_in_english: str | None = None,
    ) -> subrace.UpdateSubraceCommand:
        return subrace.UpdateSubraceCommand(
            user_id=user_id,
            subrace_id=subrace_id,
            race_id=race_id,
            name=name,
            description=description,
            increase_modifiers=increase_modifiers,
            new_features=new_features,
            add_features=add_features,
            remove_features=remove_features,
            name_in_english=name_in_english,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), subrace_id: UUID = uuid4()
    ) -> subrace.DeleteSubraceCommand:
        return subrace.DeleteSubraceCommand(user_id=user_id, subrace_id=subrace_id)


def tool_utilizes_command_factory(
    action: str = "tool_action", complexity: int = 15
) -> tool.ToolUtilizesCommand:
    return tool.ToolUtilizesCommand(action=action, complexity=complexity)


class ToolCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        tool_type: str = ToolType.ARTISANS_TOOLS.name.lower(),
        name: str = "tool_name",
        description: str = "tool_description",
        cost: coin.CoinCommand = coin_command_factory(),
        weight: weight.WeightCommand = weight_command_factory(),
        utilizes: Sequence[tool.ToolUtilizesCommand] = [
            tool_utilizes_command_factory()
        ],
    ) -> tool.CreateToolCommand:
        return tool.CreateToolCommand(
            user_id=user_id,
            tool_type=tool_type,
            name=name,
            description=description,
            cost=cost,
            weight=weight,
            utilizes=utilizes,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        tool_id: UUID = uuid4(),
        tool_type: str | None = None,
        name: str | None = None,
        description: str | None = None,
        cost: coin.CoinCommand | None = None,
        weight: weight.WeightCommand | None = None,
        utilizes: Sequence[tool.ToolUtilizesCommand] | None = None,
    ) -> tool.UpdateToolCommand:
        return tool.UpdateToolCommand(
            user_id=user_id,
            tool_id=tool_id,
            tool_type=tool_type,
            name=name,
            description=description,
            cost=cost,
            weight=weight,
            utilizes=utilizes,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), tool_id: UUID = uuid4()
    ) -> tool.DeleteToolCommand:
        return tool.DeleteToolCommand(user_id=user_id, tool_id=tool_id)


def weapon_damage_command_factory(
    dice: dice.DiceCommand = dice_command_factory(),
    damage_type: str = DamageType.SLASHING.name.lower(),
    bonus_damage: int = 0,
) -> weapon.WeaponDamageCommand:
    return weapon.WeaponDamageCommand(
        dice=dice, damage_type=damage_type, bonus_damage=bonus_damage
    )


class WeaponCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        weapon_kind_id: UUID = uuid4(),
        name: str = "weapon_name",
        description: str = "weapon_description",
        cost: coin.CoinCommand = coin_command_factory(),
        damage: weapon.WeaponDamageCommand = weapon_damage_command_factory(),
        weight: weight.WeightCommand = weight_command_factory(),
        weapon_property_ids: Sequence[UUID] = [uuid4()],
        material_id: UUID = uuid4(),
    ) -> weapon.CreateWeaponCommand:
        return weapon.CreateWeaponCommand(
            user_id=user_id,
            weapon_kind_id=weapon_kind_id,
            name=name,
            description=description,
            cost=cost,
            damage=damage,
            weight=weight,
            weapon_property_ids=weapon_property_ids,
            material_id=material_id,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        weapon_id: UUID = uuid4(),
        weapon_kind_id: UUID | None = None,
        name: str | None = None,
        description: str | None = None,
        cost: coin.CoinCommand | None = None,
        damage: weapon.WeaponDamageCommand | None = None,
        weight: weight.WeightCommand | None = None,
        weapon_property_ids: Sequence[UUID] | None = None,
        material_id: UUID | None = None,
    ) -> weapon.UpdateWeaponCommand:
        return weapon.UpdateWeaponCommand(
            user_id=user_id,
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

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), weapon_id: UUID = uuid4()
    ) -> weapon.DeleteWeaponCommand:
        return weapon.DeleteWeaponCommand(user_id=user_id, weapon_id=weapon_id)


class WeaponKindCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        weapon_type: str = WeaponType.MARTIAL_MELEE.name.lower(),
        name: str = "weapon_kind_name",
        description: str = "weapon_kind_description",
    ) -> weapon_kind.CreateWeaponKindCommand:
        return weapon_kind.CreateWeaponKindCommand(
            user_id=user_id, weapon_type=weapon_type, name=name, description=description
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        kind_id: UUID = uuid4(),
        weapon_type: str | None = None,
        name: str | None = None,
        description: str | None = None,
    ) -> weapon_kind.UpdateWeaponKindCommand:
        return weapon_kind.UpdateWeaponKindCommand(
            user_id=user_id,
            weapon_kind_id=kind_id,
            name=name,
            description=description,
            weapon_type=weapon_type,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), kind_id: UUID = uuid4()
    ) -> weapon_kind.DeleteWeaponKindCommand:
        return weapon_kind.DeleteWeaponKindCommand(
            user_id=user_id, weapon_kind_id=kind_id
        )


def weapon_property_base_range_command_factory(
    range: length.LengthCommand | None = None,
) -> weapon_property.WeaponPropertyBaseRangeCommand:
    return weapon_property.WeaponPropertyBaseRangeCommand(range=range)


def weapon_property_max_range_command_factory(
    range: length.LengthCommand | None = None,
) -> weapon_property.WeaponPropertyMaxRangeCommand:
    return weapon_property.WeaponPropertyMaxRangeCommand(range=range)


def weapon_property_second_hand_dice_command_factory(
    dice: dice.DiceCommand | None = None,
) -> weapon_property.WeaponPropertySecondHandDiceCommand:
    return weapon_property.WeaponPropertySecondHandDiceCommand(dice=dice)


class WeaponPropertyCommandFactory:
    @staticmethod
    def create(
        user_id: UUID = uuid4(),
        name: str = WeaponPropertyName.HEAVY.name.lower(),
        description: str = "weapon_property_description",
        base_range: weapon_property.WeaponPropertyBaseRangeCommand | None = None,
        max_range: weapon_property.WeaponPropertyMaxRangeCommand | None = None,
        second_hand_dice: (
            weapon_property.WeaponPropertySecondHandDiceCommand | None
        ) = None,
    ) -> weapon_property.CreateWeaponPropertyCommand:
        return weapon_property.CreateWeaponPropertyCommand(
            user_id=user_id,
            name=name,
            description=description,
            base_range=base_range,
            max_range=max_range,
            second_hand_dice=second_hand_dice,
        )

    @staticmethod
    def update(
        user_id: UUID = uuid4(),
        property_id: UUID = uuid4(),
        name: str | None = None,
        description: str | None = None,
        base_range: weapon_property.WeaponPropertyBaseRangeCommand | None = None,
        max_range: weapon_property.WeaponPropertyMaxRangeCommand | None = None,
        second_hand_dice: (
            weapon_property.WeaponPropertySecondHandDiceCommand | None
        ) = None,
    ) -> weapon_property.UpdateWeaponPropertyCommand:
        return weapon_property.UpdateWeaponPropertyCommand(
            user_id=user_id,
            weapon_property_id=property_id,
            name=name,
            description=description,
            base_range=base_range,
            max_range=max_range,
            second_hand_dice=second_hand_dice,
        )

    @staticmethod
    def delete(
        user_id: UUID = uuid4(), property_id: UUID = uuid4()
    ) -> weapon_property.DeleteWeaponPropertyCommand:
        return weapon_property.DeleteWeaponPropertyCommand(
            user_id=user_id, weapon_property_id=property_id
        )
