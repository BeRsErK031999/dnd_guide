from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.damage_type import DamageType
from domain.game_time import GameTime
from domain.length import Length
from domain.spell import Spell, SpellComponents
from ports.http.web.v1.schemas.game_time import GameTimeSchema
from ports.http.web.v1.schemas.length import LengthSchema


@dataclass
class SpellComponentsSchema:
    verbal: bool
    symbolic: bool
    material: bool
    materials: list[UUID]

    @staticmethod
    def from_domain(components: SpellComponents) -> SpellComponentsSchema:
        return SpellComponentsSchema(
            verbal=components.verbal(),
            symbolic=components.symbolic(),
            material=components.material(),
            materials=components.materials(),
        )


@dataclass
class SpellDurationSchema:
    game_time: GameTimeSchema | None

    @staticmethod
    def from_domain(duration: GameTime) -> SpellDurationSchema:
        return SpellDurationSchema(game_time=GameTimeSchema.from_domain(duration))


@dataclass
class SpellDamageTypeSchema:
    name: str | None

    @staticmethod
    def from_domain(damage_type: DamageType) -> SpellDamageTypeSchema:
        return SpellDamageTypeSchema(name=damage_type.value)


@dataclass
class SplashSchema:
    splash: LengthSchema | None

    @staticmethod
    def from_domain(splash: Length) -> SplashSchema:
        return SplashSchema(splash=LengthSchema.from_domain(splash))


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
    damage_type: SpellDamageTypeSchema | None
    duration: SpellDurationSchema | None
    casting_time: GameTimeSchema
    spell_range: LengthSchema
    splash: SplashSchema | None
    components: SpellComponentsSchema
    concentration: bool
    ritual: bool
    saving_throws: Sequence[str]
    name_in_english: str
    source_id: UUID

    @staticmethod
    def from_domain(spell: Spell) -> ReadSpellSchema:
        damage_type = spell.damage_type()
        duration = spell.duration()
        splash = spell.splash()
        return ReadSpellSchema(
            spell_id=spell.spell_id(),
            class_ids=spell.class_ids(),
            subclass_ids=spell.subclass_ids(),
            name=spell.name(),
            description=spell.description(),
            next_level_description=spell.next_level_description(),
            level=spell.level(),
            school=spell.school().value,
            damage_type=(
                SpellDamageTypeSchema.from_domain(damage_type)
                if damage_type is not None
                else None
            ),
            duration=(
                SpellDurationSchema.from_domain(duration)
                if duration is not None
                else None
            ),
            casting_time=GameTimeSchema.from_domain(spell.casting_time()),
            spell_range=LengthSchema.from_domain(spell.spell_range()),
            splash=SplashSchema.from_domain(splash) if splash is not None else None,
            components=SpellComponentsSchema.from_domain(spell.components()),
            concentration=spell.concentration(),
            ritual=spell.ritual(),
            saving_throws=spell.saving_throws(),
            name_in_english=spell.name_in_english(),
            source_id=spell.source_id(),
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
