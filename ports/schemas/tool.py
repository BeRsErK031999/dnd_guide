from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.tool import Tool, ToolUtilize
from litestar.dto import DataclassDTO
from ports.schemas.coin import CoinSchema
from ports.schemas.weight import WeightSchema


@dataclass
class ToolUtilizesSchema:
    action: str
    complexity: int

    @staticmethod
    def from_domain(tool_utilize: ToolUtilize) -> ToolUtilizesSchema:
        return ToolUtilizesSchema(
            action=tool_utilize.action(),
            complexity=tool_utilize.complexity(),
        )


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
    def from_domain(tool: Tool) -> ReadToolSchema:
        return ReadToolSchema(
            tool_id=tool.tool_id(),
            tool_type=tool.tool_type().value,
            name=tool.name(),
            description=tool.description(),
            cost=CoinSchema.from_domain(tool.cost()),
            weight=WeightSchema.from_domain(tool.weight()),
            utilizes=[
                ToolUtilizesSchema.from_domain(utilize) for utilize in tool.utilizes()
            ],
        )


@dataclass
class CreateToolSchema:
    tool_type: str
    name: str
    description: str
    cost: CoinSchema
    weight: WeightSchema
    utilizes: Sequence[ToolUtilizesSchema]


class CreateToolDTO(DataclassDTO[CreateToolSchema]):
    pass


@dataclass
class UpdateToolSchema:
    tool_type: str | None = None
    name: str | None = None
    description: str | None = None
    cost: CoinSchema | None = None
    weight: WeightSchema | None = None
    utilizes: Sequence[ToolUtilizesSchema] | None = None


class UpdateToolDTO(DataclassDTO[UpdateToolSchema]):
    pass
