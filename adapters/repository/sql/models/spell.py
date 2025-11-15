from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.damage_type import DamageType
from domain.game_time import GameTime, GameTimeUnit
from domain.length import Length, LengthUnit
from domain.modifier import Modifier
from domain.spell import Spell, SpellComponents, SpellSchool
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
    symbol_component: Mapped[bool]
    material_component: Mapped[bool]
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))

    source: Mapped[SourceModel] = relationship(back_populates="spells")
    materials: Mapped[list[MaterialComponentModel]] = relationship(
        back_populates="spells", secondary="rel_spell_material"
    )
    character_subclasses: Mapped[list[CharacterSubclassModel]] = relationship(
        back_populates="spells", secondary="rel_spell_character_subclass"
    )
    saving_throws: Mapped[list[SpellSavingThrowModel]] = relationship(
        back_populates="spell"
    )
    character_classes: Mapped[list[CharacterClassModel]] = relationship(
        back_populates="spells", secondary="rel_spell_character_class"
    )

    def to_domain(self) -> Spell:
        splash = None
        damage_type = None
        duration = None
        if self.damage_type is not None:
            damage_type = DamageType.from_str(self.damage_type)
        if self.splash is not None:
            splash = Length(count=self.splash, unit=LengthUnit.FT)
        if self.duration_count is not None and self.duration_unit is not None:
            duration = GameTime(
                count=self.duration_count,
                units=GameTimeUnit.from_str(self.duration_unit),
            )
        return Spell(
            spell_id=self.id,
            class_ids=[
                character_class.id for character_class in self.character_classes
            ],
            subclass_ids=[
                character_subclass.id
                for character_subclass in self.character_subclasses
            ],
            name=self.name,
            description=self.description,
            next_level_description=self.next_level_description,
            level=self.level,
            school=SpellSchool.from_str(self.school),
            damage_type=damage_type,
            duration=duration,
            casting_time=GameTime(
                count=self.casting_time_count,
                units=GameTimeUnit.from_str(self.casting_time_unit),
            ),
            spell_range=(Length(count=self.spell_range, unit=LengthUnit.FT)),
            splash=splash,
            components=SpellComponents(
                verbal=self.verbal_component,
                symbolic=self.symbol_component,
                material=self.material_component,
                materials=[material.id for material in self.materials],
            ),
            concentration=self.concentration,
            ritual=self.ritual,
            saving_throws=[
                saving_throw.to_domain() for saving_throw in self.saving_throws
            ],
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )

    @staticmethod
    def from_domain(spell: Spell) -> SpellModel:
        damage_type = spell.damage_type()
        duration = spell.duration()
        splash = spell.splash()
        return SpellModel(
            id=spell.spell_id(),
            name=spell.name(),
            description=spell.description(),
            name_in_english=spell.name_in_english(),
            next_level_description=spell.next_level_description(),
            level=spell.level(),
            school=spell.school().name,
            damage_type=damage_type.name if damage_type is not None else None,
            spell_range=spell.spell_range().in_ft(),
            splash=splash.in_ft() if splash is not None else None,
            duration_unit=duration.units() if duration is not None else None,
            duration_count=duration.count() if duration is not None else None,
            casting_time_unit=spell.casting_time().units(),
            casting_time_count=spell.casting_time().count(),
            concentration=spell.concentration(),
            ritual=spell.ritual(),
            verbal_component=spell.components().verbal(),
            symbol_component=spell.components().symbolic(),
            material_component=spell.components().material(),
            source_id=spell.source_id(),
        )


class SpellSavingThrowModel(Base):
    __tablename__ = "spell_saving_throw"

    name: Mapped[str]
    spell_id: Mapped[UUID] = mapped_column(ForeignKey("spell.id"))

    spell: Mapped["SpellModel"] = relationship(back_populates="saving_throws")

    def to_domain(self) -> Modifier:
        return Modifier.from_str(self.name)

    @staticmethod
    def from_domain(spell_id: UUID, modifier: Modifier) -> SpellSavingThrowModel:
        return SpellSavingThrowModel(name=modifier.name, spell_id=spell_id)


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
