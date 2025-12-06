from dataclasses import asdict, dataclass
from uuid import UUID

from application.dto.model.armor import AppArmor, AppArmorClass, AppArmorType
from ports.http.web.v1.schemas.coin import CoinSchema
from ports.http.web.v1.schemas.weight import WeightSchema


@dataclass
class ReadArmorTypeSchema:
    light_armor: str
    medium_armor: str
    heavy_armor: str
    shield: str

    @staticmethod
    def from_app() -> "ReadArmorTypeSchema":
        return ReadArmorTypeSchema(**asdict(AppArmorType.from_domain()))


@dataclass
class ArmorClassSchema:
    base_class: int
    modifier: str | None
    max_modifier_bonus: int | None

    @staticmethod
    def from_app(armor_class: AppArmorClass) -> "ArmorClassSchema":
        return ArmorClassSchema(
            base_class=armor_class.base_class,
            modifier=armor_class.modifier,
            max_modifier_bonus=armor_class.max_modifier_bonus,
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
    def from_app(armor: AppArmor) -> "ReadArmorSchema":
        return ReadArmorSchema(
            armor_id=armor.armor_id,
            armor_type=armor.armor_type,
            name=armor.name,
            description=armor.description,
            armor_class=ArmorClassSchema.from_app(armor.armor_class),
            strength=armor.strength,
            stealth=armor.stealth,
            weight=WeightSchema.from_app(armor.weight),
            cost=CoinSchema.from_app(armor.cost),
            material_id=armor.material_id,
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
    armor_id: UUID | None = None
    armor_type: str | None = None
    name: str | None = None
    description: str | None = None
    armor_class: ArmorClassSchema | None = None
    strength: int | None = None
    stealth: bool | None = None
    weight: WeightSchema | None = None
    cost: CoinSchema | None = None
    material_id: UUID | None = None
