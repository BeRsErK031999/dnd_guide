from dataclasses import dataclass
from uuid import UUID

from domain.armor import Armor, ArmorClass, ArmorType
from ports.http.web.v1.schemas.coin import CoinSchema
from ports.http.web.v1.schemas.weight import WeightSchema


@dataclass
class ReadArmorTypeSchema:
    light_armor: str
    medium_armor: str
    heavy_armor: str
    shield: str

    @staticmethod
    def from_domain() -> "ReadArmorTypeSchema":
        return ReadArmorTypeSchema(
            **{armor_type.name.lower(): armor_type.value for armor_type in ArmorType}
        )


@dataclass
class ArmorClassSchema:
    base_class: int
    modifier: str | None = None
    max_modifier_bonus: int | None = None

    @staticmethod
    def from_domain(armor_class: ArmorClass) -> "ArmorClassSchema":
        modifier = armor_class.modifier()
        return ArmorClassSchema(
            base_class=armor_class.base_class(),
            modifier=modifier.value if modifier is not None else None,
            max_modifier_bonus=armor_class.max_modifier_bonus(),
        )


@dataclass
class ReadArmorSchema:
    armor_id: UUID
    armor_type: str
    name: str
    description: str
    armor_class: ArmorClassSchema
    strength: int
    stealth: bool
    weight: WeightSchema
    cost: CoinSchema
    material_id: UUID

    @staticmethod
    def from_domain(armor: Armor) -> "ReadArmorSchema":
        return ReadArmorSchema(
            armor_id=armor.armor_id(),
            armor_type=armor.armor_type().value,
            name=armor.name(),
            description=armor.description(),
            armor_class=ArmorClassSchema.from_domain(armor.armor_class()),
            strength=armor.strength(),
            stealth=armor.stealth(),
            weight=WeightSchema.from_domain(armor.weight()),
            cost=CoinSchema.from_domain(armor.cost()),
            material_id=armor.material_id(),
        )


@dataclass
class CreateArmorSchema:
    armor_type: str
    name: str
    description: str
    armor_class: ArmorClassSchema
    strength: int
    stealth: bool
    weight: WeightSchema
    cost: CoinSchema
    material_id: UUID


@dataclass
class UpdateArmorSchema:
    armor_id: UUID
    armor_type: str | None = None
    name: str | None = None
    description: str | None = None
    armor_class: ArmorClassSchema | None = None
    strength: int | None = None
    stealth: bool | None = None
    weight: WeightSchema | None = None
    cost: CoinSchema | None = None
    material_id: UUID | None = None
