from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClassModel
    from adapters.repository.sql.models.character_subclass import CharacterSubclassModel
    from adapters.repository.sql.models.material_component import MaterialComponentModel
    from adapters.repository.sql.models.source import SourceModel


class SpellModel(Base):
    __tablename__ = "spell"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    next_level_description: Mapped[str]
    level: Mapped[int]
    school: Mapped[str]
    damage_type: Mapped[str | None]
    spell_range: Mapped[float]
    splash: Mapped[float | None]
    concentration: Mapped[bool]
    ritual: Mapped[bool]
    verbal_component: Mapped[bool]
    symbol_component: Mapped[bool]
    material_component: Mapped[bool]
    duration: Mapped[SpellDurationModel] = relationship(back_populates="spell")
    casting_time: Mapped[SpellCastingTimeModel] = relationship(back_populates="spell")
    saving_throws: Mapped[list[SpellSavingThrowModel]] = relationship(
        back_populates="spell"
    )
    character_classes: Mapped[list[CharacterClassModel]] = relationship(
        back_populates="spells", secondary="rel_spell_character_class"
    )
    character_subclasses: Mapped[list[CharacterSubclassModel] | None] = relationship(
        back_populates="spells", secondary="rel_spell_character_subclass"
    )
    materials: Mapped[list[MaterialComponentModel] | None] = relationship(
        back_populates="spells", secondary="rel_spell_material"
    )
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))
    source: Mapped[SourceModel] = relationship(back_populates="spells")


class SpellDurationModel(Base):
    __tablename__ = "spell_duration"

    units: Mapped[str]
    count: Mapped[int]
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"), unique=True)
    spell: Mapped["SpellModel"] = relationship(back_populates="duration")


class SpellCastingTimeModel(Base):
    __tablename__ = "spell_casting_time"

    units: Mapped[str]
    count: Mapped[int]
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"), unique=True)
    spell: Mapped["SpellModel"] = relationship(back_populates="casting_time")


class SpellSavingThrowModel(Base):
    __tablename__ = "spell_saving_throw"

    name: Mapped[str]
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))
    spell: Mapped["SpellModel"] = relationship(back_populates="saving_throws")


class RelSpellCharacterClassModel(Base):
    __tablename__ = "rel_spell_character_class"

    character_class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))


class RelSpellCharacterSubclassModel(Base):
    __tablename__ = "rel_spell_character_subclass"

    character_subclass_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_subclass.id")
    )
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))


class RelSpellMaterialModel(Base):
    __tablename__ = "rel_spell_material"

    material_id: Mapped[UUID] = mapped_column(ForeignKey("material.id"))
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))
