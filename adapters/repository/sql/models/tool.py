from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.coin import AppCoins
from application.dto.model.tool import AppTool, AppToolUtilizes
from application.dto.model.weight import AppWeight
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

    utilizes: Mapped[list["ToolUtilizeModel"]] = relationship(
        back_populates="tool", cascade="all, delete-orphan"
    )
    character_classes: Mapped[list["CharacterClassModel"]] = relationship(
        back_populates="tools", secondary="rel_class_tool"
    )

    def to_app(self) -> AppTool:
        return AppTool(
            tool_id=self.id,
            tool_type=self.tool_type,
            name=self.name,
            description=self.description,
            cost=AppCoins(count=self.cost),
            weight=AppWeight(count=self.weight),
            utilizes=[utilize.to_app() for utilize in self.utilizes],
        )

    @staticmethod
    def from_app(domain_tool: AppTool) -> "ToolModel":
        return ToolModel(
            id=domain_tool.tool_id,
            tool_type=domain_tool.tool_type,
            name=domain_tool.name,
            description=domain_tool.description,
            cost=domain_tool.cost.count,
            weight=domain_tool.weight.count,
        )


class ToolUtilizeModel(Base):
    __tablename__ = "tool_utilize"

    action: Mapped[str]
    complexity: Mapped[int]
    tool_id: Mapped[UUID] = mapped_column(ForeignKey("tool.id", ondelete="cascade"))

    tool: Mapped["ToolModel"] = relationship(back_populates="utilizes")

    def to_app(self) -> AppToolUtilizes:
        return AppToolUtilizes(
            action=self.action,
            complexity=self.complexity,
        )

    @staticmethod
    def from_app(tool_id: UUID, tool_utilize: AppToolUtilizes) -> "ToolUtilizeModel":
        return ToolUtilizeModel(
            action=tool_utilize.action,
            complexity=tool_utilize.complexity,
            tool_id=tool_id,
        )
