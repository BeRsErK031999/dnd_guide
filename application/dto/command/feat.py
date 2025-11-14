from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.error import DomainError


@dataclass
class FeatRequiredModifierCommand:
    modifier: str
    min_value: int


@dataclass
class CreateFeatCommand:
    user_id: UUID
    name: str
    description: str
    is_caster: bool
    required_armor_types: Sequence[str]
    required_modifiers: Sequence[FeatRequiredModifierCommand]
    increase_modifiers: Sequence[str]


@dataclass
class UpdateFeatCommand:
    user_id: UUID
    feat_id: UUID
    name: str | None = None
    description: str | None = None
    is_caster: bool | None = None
    required_armor_types: Sequence[str] | None = None
    required_modifiers: Sequence[FeatRequiredModifierCommand] | None = None
    increase_modifiers: Sequence[str] | None = None

    def __post_init__(self) -> None:
        if all(
            [
                self.name is None,
                self.description is None,
                self.is_caster is None,
                self.required_armor_types is None,
                self.required_modifiers is None,
                self.increase_modifiers is None,
            ]
        ):
            raise DomainError.invalid_data("не переданы данные для обновления черты")


@dataclass
class DeleteFeatCommand:
    user_id: UUID
    feat_id: UUID
