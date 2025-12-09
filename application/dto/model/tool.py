from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.tool import Tool, ToolType, ToolUtilize

from .coin import AppCoins
from .weight import AppWeight

__all__ = ["AppToolType", "AppToolUtilizes", "AppTool"]


@dataclass
class AppToolType:
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
    def from_domain() -> "AppToolType":
        return AppToolType(
            **{tool_type.name.lower(): tool_type.value for tool_type in ToolType}
        )


@dataclass
class AppToolUtilizes:
    action: str
    complexity: int

    @staticmethod
    def from_domain(tool_utilize: ToolUtilize) -> "AppToolUtilizes":
        return AppToolUtilizes(
            action=tool_utilize.action(),
            complexity=tool_utilize.complexity(),
        )

    def to_domain(self) -> ToolUtilize:
        return ToolUtilize(
            action=self.action,
            complexity=self.complexity,
        )


@dataclass
class AppTool:
    tool_id: UUID
    tool_type: str
    name: str
    description: str
    cost: AppCoins
    weight: AppWeight
    utilizes: Sequence[AppToolUtilizes]

    @staticmethod
    def from_domain(tool: Tool) -> "AppTool":
        return AppTool(
            tool_id=tool.tool_id(),
            tool_type=tool.tool_type().value,
            name=tool.name(),
            description=tool.description(),
            cost=AppCoins.from_domain(tool.cost()),
            weight=AppWeight.from_domain(tool.weight()),
            utilizes=[
                AppToolUtilizes.from_domain(utilize) for utilize in tool.utilizes()
            ],
        )

    def to_domain(self) -> Tool:
        return Tool(
            tool_id=self.tool_id,
            tool_type=ToolType.from_str(self.tool_type),
            name=self.name,
            description=self.description,
            cost=self.cost.to_domain(),
            weight=self.weight.to_domain(),
            utilizes=[u.to_domain() for u in self.utilizes],
        )
