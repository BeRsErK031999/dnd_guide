from dataclasses import asdict, dataclass
from uuid import UUID

from application.dto.command.armor import (
    ArmorClassCommand,
    CreateArmorCommand,
    UpdateArmorCommand,
)
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

    def to_command(self) -> ArmorClassCommand:
        return ArmorClassCommand(
            base_class=self.base_class,
            modifier=self.modifier,
            max_modifier_bonus=self.max_modifier_bonus,
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

    def to_command(self, user_id: UUID) -> CreateArmorCommand:
        return CreateArmorCommand(
            user_id=user_id,
            armor_type=self.armor_type,
            name=self.name,
            description=self.description,
            armor_class=self.armor_class.to_command(),
            strength=self.strength,
            stealth=self.stealth,
            weight=self.weight.to_command(),
            cost=self.cost.to_command(),
            material_id=self.material_id,
        )


@dataclass
class UpdateArmorSchema:
    armor_type: str | None = None
    name: str | None = None
    description: str | None = None
    armor_class: ArmorClassSchema | None = None
    strength: int | None = None
    stealth: bool | None = None
    weight: WeightSchema | None = None
    cost: CoinSchema | None = None
    material_id: UUID | None = None

    def to_command(self, user_id: UUID, armor_id: UUID) -> UpdateArmorCommand:
        return UpdateArmorCommand(
            user_id=user_id,
            armor_id=armor_id,
            armor_type=self.armor_type,
            name=self.name,
            description=self.description,
            armor_class=(
                self.armor_class.to_command() if self.armor_class is not None else None
            ),
            strength=self.strength,
            stealth=self.stealth,
            weight=self.weight.to_command() if self.weight is not None else None,
            cost=self.cost.to_command() if self.cost is not None else None,
            material_id=self.material_id,
        )
