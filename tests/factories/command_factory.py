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
from domain.dice import DiceType
from domain.game_time import GameTimeUnit
from domain.length import LengthUnit
from domain.modifier import Modifier
from domain.skill import Skill
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
