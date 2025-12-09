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
from domain.length import LengthUnit
from domain.modifier import Modifier
from domain.weight import WeightUnit


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
