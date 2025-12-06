from dataclasses import asdict, dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.spell import (
    CreateSpellCommand,
    SpellComponentsCommand,
    SpellDamageTypeCommand,
    SpellDurationCommand,
    SplashCommand,
    UpdateSpellCommand,
)
from application.dto.model.spell import AppSpell, AppSpellComponents, AppSpellSchool
from ports.http.web.v1.schemas.game_time import GameTimeSchema
from ports.http.web.v1.schemas.length import LengthSchema


@dataclass
class SpellComponentsSchema:
    verbal: bool
    symbolic: bool
    material: bool
    materials: list[UUID]

    @staticmethod
    def from_app(components: AppSpellComponents) -> "SpellComponentsSchema":
        return SpellComponentsSchema(
            verbal=components.verbal,
            symbolic=components.symbolic,
            material=components.material,
            materials=components.materials,
        )

    def to_command(self) -> SpellComponentsCommand:
        return SpellComponentsCommand(
            verbal=self.verbal,
            symbolic=self.symbolic,
            material=self.material,
            materials=self.materials,
        )


@dataclass
class SpellDurationSchema:
    game_time: GameTimeSchema | None

    def to_command(self) -> SpellDurationCommand:
        return SpellDurationCommand(
            game_time=(
                self.game_time.to_command() if self.game_time is not None else None
            )
        )


@dataclass
class SpellDamageTypeSchema:
    name: str | None

    def to_command(self) -> SpellDamageTypeCommand:
        return SpellDamageTypeCommand(name=self.name)


@dataclass
class SplashSchema:
    splash: LengthSchema | None

    def to_command(self) -> SplashCommand:
        return SplashCommand(
            splash=self.splash.to_command() if self.splash is not None else None
        )


@dataclass
class ReadSpellSchoolSchema:
    abjuration: str
    conjuration: str
    divination: str
    enchantment: str
    evocation: str
    illusion: str
    necromancy: str
    transmutation: str

    @staticmethod
    def from_domain() -> "ReadSpellSchoolSchema":
        return ReadSpellSchoolSchema(**asdict(AppSpellSchool.from_domain()))


@dataclass
class ReadSpellSchema:
    spell_id: UUID
    class_ids: Sequence[UUID]
    subclass_ids: Sequence[UUID]
    name: str
    description: str
    next_level_description: str
    level: int
    school: str
    damage_type: str | None
    duration: GameTimeSchema | None
    casting_time: GameTimeSchema
    spell_range: LengthSchema
    splash: LengthSchema | None
    components: SpellComponentsSchema
    concentration: bool
    ritual: bool
    saving_throws: Sequence[str]
    name_in_english: str
    source_id: UUID

    @staticmethod
    def from_app(spell: AppSpell) -> "ReadSpellSchema":
        return ReadSpellSchema(
            spell_id=spell.spell_id,
            class_ids=spell.class_ids,
            subclass_ids=spell.subclass_ids,
            name=spell.name,
            description=spell.description,
            next_level_description=spell.next_level_description,
            level=spell.level,
            school=spell.school,
            damage_type=spell.damage_type,
            duration=(
                GameTimeSchema.from_app(spell.duration)
                if spell.duration is not None
                else None
            ),
            casting_time=GameTimeSchema.from_app(spell.casting_time),
            spell_range=LengthSchema.from_app(spell.spell_range),
            splash=(
                LengthSchema.from_app(spell.splash)
                if spell.splash is not None
                else None
            ),
            components=SpellComponentsSchema.from_app(spell.components),
            concentration=spell.concentration,
            ritual=spell.ritual,
            saving_throws=spell.saving_throws,
            name_in_english=spell.name_in_english,
            source_id=spell.source_id,
        )


@dataclass
class CreateSpellSchema:
    class_ids: Sequence[UUID]
    subclass_ids: Sequence[UUID]
    name: str
    description: str
    next_level_description: str
    level: int
    school: str
    damage_type: SpellDamageTypeSchema
    duration: SpellDurationSchema
    casting_time: GameTimeSchema
    spell_range: LengthSchema
    splash: SplashSchema
    components: SpellComponentsSchema
    concentration: bool
    ritual: bool
    saving_throws: Sequence[str]
    name_in_english: str
    source_id: UUID

    def to_command(self, user_id: UUID) -> CreateSpellCommand:
        return CreateSpellCommand(
            user_id=user_id,
            class_ids=self.class_ids,
            subclass_ids=self.subclass_ids,
            name=self.name,
            description=self.description,
            next_level_description=self.next_level_description,
            level=self.level,
            school=self.school,
            damage_type=self.damage_type.to_command(),
            duration=self.duration.to_command(),
            casting_time=self.casting_time.to_command(),
            spell_range=self.spell_range.to_command(),
            splash=self.splash.to_command(),
            components=self.components.to_command(),
            concentration=self.concentration,
            ritual=self.ritual,
            saving_throws=self.saving_throws,
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )


@dataclass
class UpdateSpellSchema:
    class_ids: Sequence[UUID] | None = None
    subclass_ids: Sequence[UUID] | None = None
    name: str | None = None
    description: str | None = None
    next_level_description: str | None = None
    level: int | None = None
    school: str | None = None
    damage_type: SpellDamageTypeSchema | None = None
    duration: SpellDurationSchema | None = None
    casting_time: GameTimeSchema | None = None
    spell_range: LengthSchema | None = None
    splash: SplashSchema | None = None
    components: SpellComponentsSchema | None = None
    concentration: bool | None = None
    ritual: bool | None = None
    saving_throws: Sequence[str] | None = None
    name_in_english: str | None = None
    source_id: UUID | None = None

    def to_command(self, user_id: UUID, spell_id: UUID) -> UpdateSpellCommand:
        return UpdateSpellCommand(
            user_id=user_id,
            spell_id=spell_id,
            class_ids=self.class_ids,
            subclass_ids=self.subclass_ids,
            name=self.name,
            description=self.description,
            next_level_description=self.next_level_description,
            level=self.level,
            school=self.school,
            damage_type=(
                self.damage_type.to_command() if self.damage_type is not None else None
            ),
            duration=self.duration.to_command() if self.duration is not None else None,
            casting_time=(
                self.casting_time.to_command()
                if self.casting_time is not None
                else None
            ),
            spell_range=(
                self.spell_range.to_command() if self.spell_range is not None else None
            ),
            splash=self.splash.to_command() if self.splash is not None else None,
            components=(
                self.components.to_command() if self.components is not None else None
            ),
            concentration=self.concentration,
            ritual=self.ritual,
            saving_throws=self.saving_throws,
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )
