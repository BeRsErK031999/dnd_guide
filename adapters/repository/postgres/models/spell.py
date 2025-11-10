from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.postgres.models.base import Base
from adapters.repository.postgres.models.mixin import Timestamp
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.postgres.models.character_class import CharacterClass
    from adapters.repository.postgres.models.character_subclass import CharacterSubclass
    from adapters.repository.postgres.models.material_component import MaterialComponent


class Spell(Timestamp, Base):
    __tablename__ = "spell"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(100))
    next_level_description: Mapped[str]
    level: Mapped[int]
    school: Mapped[str]
    damage_type: Mapped[str | None]
    spell_range: Mapped[float]
    concentration: Mapped[bool]
    ritual: Mapped[bool]
    verbal_component: Mapped[bool]
    symbol_component: Mapped[bool]
    material_component: Mapped[bool]
    duration: Mapped["SpellDuration"] = relationship(back_populates="spell")
    casting_time: Mapped["SpellCastingTime"] = relationship(back_populates="spell")
    saving_throws: Mapped[list["SpellSavingThrow"]] = relationship(
        back_populates="spell"
    )
    character_classes: Mapped[list["CharacterClass"]] = relationship(
        back_populates="spells", secondary="rel_spell_character_class"
    )
    character_subclasses: Mapped[list["CharacterSubclass"] | None] = relationship(
        back_populates="spells", secondary="rel_spell_character_subclass"
    )
    materials: Mapped[list["MaterialComponent"] | None] = relationship(
        back_populates="spells", secondary="rel_spell_material"
    )


class SpellDuration(Timestamp, Base):
    __tablename__ = "spell_duration"

    units: Mapped[str]
    count: Mapped[int]
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"), unique=True)
    spell: Mapped["Spell"] = relationship(back_populates="duration")


class SpellCastingTime(Timestamp, Base):
    __tablename__ = "spell_casting_time"

    units: Mapped[str]
    count: Mapped[int]
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"), unique=True)
    spell: Mapped["Spell"] = relationship(back_populates="casting_time")


class SpellSavingThrow(Timestamp, Base):
    __tablename__ = "spell_saving_throw"

    name: Mapped[str]
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))
    spell: Mapped["Spell"] = relationship(back_populates="saving_throws")


class RelSpellCharacterClass(Timestamp, Base):
    __tablename__ = "rel_spell_character_class"

    character_class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))


class RelSpellCharacterSubclass(Timestamp, Base):
    __tablename__ = "rel_spell_character_subclass"

    character_subclass_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_subclass.id")
    )
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))


class RelSpellMaterial(Timestamp, Base):
    __tablename__ = "rel_spell_material"

    material_id: Mapped[UUID] = mapped_column(ForeignKey("material.id"))
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))
