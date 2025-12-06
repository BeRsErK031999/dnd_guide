from dataclasses import asdict, dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.tool import (
    CreateToolCommand,
    ToolUtilizesCommand,
    UpdateToolCommand,
)
from application.dto.model.tool import AppTool, AppToolType, AppToolUtilizes
from ports.http.web.v1.schemas.coin import CoinSchema
from ports.http.web.v1.schemas.weight import WeightSchema


@dataclass
class ReadToolTypeSchema:
    artisans_tools: str
    gaming_sets: str
    musical_instruments: str
    thieves_tools: str
    disguise_kit: str
    forgery_kit: str
    herbalism_kit: str
    navigators_tools: str
    poisoners_kit: str

    @staticmethod
    def from_domain() -> "ReadToolTypeSchema":
        return ReadToolTypeSchema(**asdict(AppToolType.from_domain()))


@dataclass
class ToolUtilizesSchema:
    action: str
    complexity: int

    @staticmethod
    def from_app(tool_utilize: AppToolUtilizes) -> "ToolUtilizesSchema":
        return ToolUtilizesSchema(
            action=tool_utilize.action, complexity=tool_utilize.complexity
        )

    def to_command(self) -> ToolUtilizesCommand:
        return ToolUtilizesCommand(action=self.action, complexity=self.complexity)


@dataclass
class ReadToolSchema:
    tool_id: UUID
    tool_type: str
    name: str
    description: str
    cost: CoinSchema
    weight: WeightSchema
    utilizes: Sequence[ToolUtilizesSchema]

    @staticmethod
    def from_app(tool: AppTool) -> "ReadToolSchema":
        return ReadToolSchema(
            tool_id=tool.tool_id,
            tool_type=tool.tool_type,
            name=tool.name,
            description=tool.description,
            cost=CoinSchema.from_app(tool.cost),
            weight=WeightSchema.from_app(tool.weight),
            utilizes=[ToolUtilizesSchema.from_app(u) for u in tool.utilizes],
        )


@dataclass
class CreateToolSchema:
    tool_type: str
    name: str
    description: str
    cost: CoinSchema
    weight: WeightSchema
    utilizes: Sequence[ToolUtilizesSchema]

    def to_command(self, user_id: UUID) -> CreateToolCommand:
        return CreateToolCommand(
            user_id=user_id,
            tool_type=self.tool_type,
            name=self.name,
            description=self.description,
            cost=self.cost.to_command(),
            weight=self.weight.to_command(),
            utilizes=[u.to_command() for u in self.utilizes],
        )


@dataclass
class UpdateToolSchema:
    tool_type: str | None = None
    name: str | None = None
    description: str | None = None
    cost: CoinSchema | None = None
    weight: WeightSchema | None = None
    utilizes: Sequence[ToolUtilizesSchema] | None = None

    def to_command(self, user_id: UUID, tool_id: UUID) -> UpdateToolCommand:
        u = self.utilizes
        if u is not None:
            u = [ut.to_command() for ut in u]
        return UpdateToolCommand(
            user_id=user_id,
            tool_id=tool_id,
            tool_type=self.tool_type,
            name=self.name,
            description=self.description,
            cost=self.cost.to_command() if self.cost else None,
            weight=self.weight.to_command() if self.weight else None,
            utilizes=u,
        )
