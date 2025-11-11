from dataclasses import dataclass
from uuid import UUID

from application.dto.command.coin import CoinCommand
from application.dto.command.weight import WeightCommand
from domain.error import DomainError


@dataclass
class ArmorClassCommand:
    base_class: int
    modifier: str | None = None
    max_modifier_bonus: int | None = None


@dataclass
class CreateArmorCommand:
    user_id: UUID
    armor_type: str
    name: str
    description: str
    armor_class: ArmorClassCommand
    strength: int
    stealth: bool
    weight: WeightCommand
    cost: CoinCommand
    material_id: UUID


@dataclass
class UpdateArmorCommand:
    user_id: UUID
    armor_id: UUID
    armor_type: str | None = None
    name: str | None = None
    description: str | None = None
    armor_class: ArmorClassCommand | None = None
    strength: int | None = None
    stealth: bool | None = None
    weight: WeightCommand | None = None
    cost: CoinCommand | None = None
    material_id: UUID | None = None

    def __post_init__(self) -> None:
        if all(
            [
                self.armor_type is None,
                self.name is None,
                self.description is None,
                self.armor_class is None,
                self.strength is None,
                self.stealth is None,
                self.weight is None,
                self.cost is None,
                self.material_id is None,
            ]
        ):
            raise DomainError.invalid_data("не переданы данные для обновления доспехов")


@dataclass
class DeleteArmorCommand:
    user_id: UUID
    armor_id: UUID
