from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.coin import Coins
from domain.tool import Tool
from domain.tool.tool_type import ToolType
from domain.tool.utilize import ToolUtilize
from domain.weight import Weight, WeightUnit
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClassModel


class ToolModel(Base):
    __tablename__ = "tool"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    cost: Mapped[int]
    weight: Mapped[float]
    tool_type: Mapped[str]

    utilizes: Mapped[list[ToolUtilizeModel]] = relationship(
        back_populates="tools", cascade="all, delete-orphan"
    )
    character_classes: Mapped[list[CharacterClassModel]] = relationship(
        back_populates="tools", secondary="rel_class_tool"
    )

    def to_domain_tool(self) -> Tool:
        return Tool(
            tool_id=self.id,
            tool_type=ToolType.from_str(self.tool_type),
            name=self.name,
            description=self.description,
            cost=Coins(count=self.cost),
            weight=Weight(count=self.weight, unit=WeightUnit.LB),
            utilizes=[utilize.to_domain_tool_utilize() for utilize in self.utilizes],
        )

    @staticmethod
    def from_domain_tool(domain_tool: Tool) -> ToolModel:
        return ToolModel(
            id=domain_tool.tool_id(),
            tool_type=domain_tool.tool_type().name,
            name=domain_tool.name(),
            description=domain_tool.description(),
            cost=domain_tool.cost().in_copper(),
            weight=domain_tool.weight().in_lb(),
        )


class ToolUtilizeModel(Base):
    __tablename__ = "tool_utilize"

    action: Mapped[str]
    complexity: Mapped[int]
    tool_id: Mapped[UUID] = mapped_column(ForeignKey("tool.id", ondelete="cascade"))
    tool: Mapped[ToolModel] = relationship(back_populates="utilizes")

    def to_domain_tool_utilize(self) -> ToolUtilize:
        return ToolUtilize(
            action=self.action,
            complexity=self.complexity,
        )

    @staticmethod
    def from_domain_tool_utilize(
        tool_id: UUID, tool_utilize: ToolUtilize
    ) -> ToolUtilizeModel:
        return ToolUtilizeModel(
            action=tool_utilize.action,
            complexity=tool_utilize.complexity,
            tool_id=tool_id,
        )
