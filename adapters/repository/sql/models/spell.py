from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.game_time import AppGameTime
from application.dto.model.length import AppLength
from application.dto.model.spell import AppSpell, AppSpellComponents
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
    duration_unit: Mapped[str | None]
    duration_count: Mapped[int | None]
    casting_time_unit: Mapped[str]
    casting_time_count: Mapped[int]
    concentration: Mapped[bool]
    ritual: Mapped[bool]
    verbal_component: Mapped[bool]
    symbolic_component: Mapped[bool]
    material_component: Mapped[bool]
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))

    source: Mapped["SourceModel"] = relationship(back_populates="spells")
    materials: Mapped[list["MaterialComponentModel"]] = relationship(
        back_populates="spells", secondary="rel_spell_material"
    )
    character_subclasses: Mapped[list["CharacterSubclassModel"]] = relationship(
        back_populates="spells", secondary="rel_spell_character_subclass"
    )
    saving_throws: Mapped[list["SpellSavingThrowModel"]] = relationship(
        back_populates="spell"
    )
    character_classes: Mapped[list["CharacterClassModel"]] = relationship(
        back_populates="spells", secondary="rel_spell_character_class"
    )

    def to_app(self) -> AppSpell:
        duration = None
        splash = None
        if self.duration_count is not None and self.duration_unit is not None:
            duration = AppGameTime(
                count=self.duration_count,
                unit=self.duration_unit,
            )
        if self.splash is not None:
            splash = AppLength(count=self.splash)
        return AppSpell(
            spell_id=self.id,
            class_ids=[c.id for c in self.character_classes],
            subclass_ids=[c.id for c in self.character_subclasses],
            name=self.name,
            description=self.description,
            next_level_description=self.next_level_description,
            level=self.level,
            school=self.school,
            damage_type=self.damage_type,
            duration=duration,
            casting_time=AppGameTime(self.casting_time_count, self.casting_time_unit),
            spell_range=AppLength(count=self.spell_range),
            splash=splash,
            components=AppSpellComponents(
                self.verbal_component,
                self.symbolic_component,
                self.material_component,
                [m.id for m in self.materials],
            ),
            concentration=self.concentration,
            ritual=self.ritual,
            saving_throws=[m.to_app() for m in self.saving_throws],
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )

    @staticmethod
    def from_app(spell: AppSpell) -> "SpellModel":
        duration = spell.duration
        splash = spell.splash
        return SpellModel(
            id=spell.spell_id,
            name=spell.name,
            description=spell.description,
            name_in_english=spell.name_in_english,
            next_level_description=spell.next_level_description,
            level=spell.level,
            school=spell.school,
            damage_type=spell.damage_type,
            spell_range=spell.spell_range.count,
            splash=splash.count if splash is not None else None,
            duration_unit=duration.unit if duration is not None else None,
            duration_count=duration.count if duration is not None else None,
            casting_time_unit=spell.casting_time.unit,
            casting_time_count=spell.casting_time.count,
            concentration=spell.concentration,
            ritual=spell.ritual,
            verbal_component=spell.components.verbal,
            symbol_component=spell.components.symbolic,
            material_component=spell.components.material,
            source_id=spell.source_id,
        )


class SpellSavingThrowModel(Base):
    __tablename__ = "spell_saving_throw"

    name: Mapped[str]
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))

    spell: Mapped["SpellModel"] = relationship(back_populates="saving_throws")

    def to_app(self) -> str:
        return self.name

    @staticmethod
    def from_app(spell_id: UUID, name: str) -> "SpellSavingThrowModel":
        return SpellSavingThrowModel(name=name, spell_id=spell_id)


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

    material_id: Mapped[UUID] = mapped_column(ForeignKey("material_component.id"))
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))
