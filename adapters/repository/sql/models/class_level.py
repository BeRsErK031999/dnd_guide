from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClass


class ClassLevel(Base):
    __tablename__ = "class_level"

    level: Mapped[int]
    dice_name: Mapped[str | None]
    dice_description: Mapped[str | None]
    number_cantrips_know: Mapped[int | None]
    number_spells_know: Mapped[int | None]
    number_arcanums_know: Mapped[int | None]
    points: Mapped[int | None]
    points_description: Mapped[str | None]
    bonus_damage: Mapped[int | None]
    bonus_damage_description: Mapped[str | None]
    increase_speed: Mapped[float | None]
    increase_speed_description: Mapped[str | None]
    character_class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClass"] = relationship(
        back_populates="class_levels"
    )
    class_level_spell_slots: Mapped[list["ClassLevelSpellSlot"] | None] = relationship(
        back_populates="class_level"
    )


class ClassLevelSpellSlot(Base):
    __tablename__ = "class_level_spell_slot"

    level_1: Mapped[int]
    level_2: Mapped[int]
    level_3: Mapped[int]
    level_4: Mapped[int]
    level_5: Mapped[int]
    level_6: Mapped[int]
    level_7: Mapped[int]
    level_8: Mapped[int]
    level_9: Mapped[int]
    class_level_id: Mapped[UUID] = mapped_column(ForeignKey("class_level.id"))
    class_level: Mapped["ClassLevel"] = relationship(
        back_populates="class_level_spell_slots"
    )
