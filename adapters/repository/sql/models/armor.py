from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Armor(Timestamp, Base):
    __tablename__ = "armor"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    armor_type: Mapped[str]
    strength: Mapped[int]
    stealth: Mapped[bool]
    weight: Mapped[float]
    cost: Mapped[float]
    base_class: Mapped[int]
    modifier: Mapped[str] = mapped_column(String(50), nullable=True)
    max_modifier_bonus: Mapped[int | None]
