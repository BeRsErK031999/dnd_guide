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
from domain.modifier import Modifier
from domain.weight import WeightUnit


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
    base_class: int = 10,
    modifier: Modifier | None = None,
    max_modifier_bonus: int | None = None,
    weight_count: float = 10,
    weight_unit: str = WeightUnit.LB.name.lower(),
    cost_count: int = 10,
    piece_type: str = PieceType.COPPER.name.lower(),
    material_id: UUID = uuid4(),
) -> armor.AppArmor:
    return armor.AppArmor(
        armor_id=armor_id,
        armor_type=armor_type,
        name=name,
        description=description,
        armor_class=armor_class_model_factory(
            base_class=base_class,
            modifier=modifier,
            max_modifier_bonus=max_modifier_bonus,
        ),
        strength=strength,
        stealth=stealth,
        weight=weight_model_factory(count=weight_count, unit=weight_unit),
        cost=coins_model_factory(count=cost_count, piece_type=piece_type),
        material_id=material_id,
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
