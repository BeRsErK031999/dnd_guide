from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.error import DomainError


@dataclass
class SubraceFeatureCommand:
    name: str
    description: str


@dataclass
class SubraceIncreaseModifierCommand:
    modifier: str
    bonus: int


@dataclass
class CreateSubraceCommand:
    user_id: UUID
    race_id: UUID
    name: str
    description: str
    increase_modifiers: Sequence[SubraceIncreaseModifierCommand]
    features: Sequence[SubraceFeatureCommand] = []


@dataclass
class UpdateSubraceCommand:
    user_id: UUID
    subrace_id: UUID
    race_id: UUID
    name: str | None = None
    description: str | None = None
    increase_modifiers: Sequence[SubraceIncreaseModifierCommand] | None = None
    new_features: Sequence[SubraceFeatureCommand] | None = None
    add_features: Sequence[SubraceFeatureCommand] | None = None
    remove_features: Sequence[str] | None = None

    def __post_init__(self) -> None:
        if all(
            [
                self.race_id is None,
                self.name is None,
                self.description is None,
                self.increase_modifiers is None,
                self.new_features is None,
                self.add_features is None,
                self.remove_features is None,
            ]
        ):
            raise DomainError.invalid_data("не переданы данные для обновления расы")
        if self.new_features is not None and (
            self.add_features is not None or self.remove_features is not None
        ):
            raise DomainError.invalid_data(
                "для умений расы нельзя одновременно назначить новый список и "
                "корректировать существующий"
            )
        if self.add_features is not None and self.remove_features is not None:
            for feature in self.add_features:
                if feature.name in self.remove_features:
                    raise DomainError.invalid_data(
                        f"умение с названием {feature.name} есть в списке для "
                        "удаления и для добавления"
                    )


@dataclass
class DeleteSubraceCommand:
    user_id: UUID
    subrace_id: UUID
