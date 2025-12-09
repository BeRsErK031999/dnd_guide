from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.coin import CoinCommand
from application.dto.command.weight import WeightCommand
from domain.error import DomainError

__all__ = [
    "ToolUtilizesCommand",
    "CreateToolCommand",
    "UpdateToolCommand",
    "DeleteToolCommand",
]


@dataclass
class ToolUtilizesCommand:
    action: str
    complexity: int


@dataclass
class CreateToolCommand:
    user_id: UUID
    tool_type: str
    name: str
    description: str
    cost: CoinCommand
    weight: WeightCommand
    utilizes: Sequence[ToolUtilizesCommand]


@dataclass
class UpdateToolCommand:
    user_id: UUID
    tool_id: UUID
    tool_type: str | None = None
    name: str | None = None
    description: str | None = None
    cost: CoinCommand | None = None
    weight: WeightCommand | None = None
    utilizes: Sequence[ToolUtilizesCommand] | None = None

    def __post_init__(self):
        if all(
            [
                self.tool_type is None,
                self.name is None,
                self.description is None,
                self.cost is None,
                self.weight is None,
                self.utilizes is None,
            ]
        ):
            raise DomainError.invalid_data(
                "не переданы данные для обновления инструмента"
            )


@dataclass
class DeleteToolCommand:
    user_id: UUID
    tool_id: UUID
