from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.postgres.models.base import Base
from adapters.repository.postgres.models.mixin import Timestamp
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.postgres.models.character_class import CharacterClass


class Tool(Timestamp, Base):
    __tablename__ = "tool"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    cost: Mapped[int]
    weight: Mapped[float]
    tool_type: Mapped[str]
    utilizes: Mapped[list["ToolUtilize"]] = relationship(
        back_populates="tools", secondary="rel_tool_utilize"
    )
    character_classes: Mapped[list["CharacterClass"]] = relationship(
        back_populates="tools", secondary="rel_class_tool"
    )


class ToolUtilize(Timestamp, Base):
    __tablename__ = "tool_utilize"

    action: Mapped[str]
    complexity: Mapped[int]
    tool_id: Mapped[UUID] = mapped_column(ForeignKey("tool.id"))
    tools: Mapped["Tool"] = relationship(back_populates="utilizes")
