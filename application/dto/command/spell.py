from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.game_time import GameTimeCommand
from application.dto.command.length import LengthCommand
from domain.error import DomainError


@dataclass
class SpellComponentsCommand:
    verbal: bool
    symbolic: bool
    material: bool
    materials: list[UUID]


@dataclass
class SpellDurationCommand:
    game_time: GameTimeCommand | None


@dataclass
class SpellDamageTypeCommand:
    name: str | None


@dataclass
class SplashCommand:
    splash: LengthCommand | None


@dataclass
class CreateSpellCommand:
    user_id: UUID
    class_ids: Sequence[UUID]
    subclass_ids: Sequence[UUID]
    name: str
    description: str
    next_level_description: str
    level: int
    school: str
    damage_type: SpellDamageTypeCommand
    duration: SpellDurationCommand
    casting_time: GameTimeCommand
    spell_range: LengthCommand
    splash: SplashCommand
    components: SpellComponentsCommand
    concentration: bool
    ritual: bool
    saving_throws: Sequence[str]
    name_in_english: str
    source_id: UUID


@dataclass
class UpdateSpellCommand:
    user_id: UUID
    spell_id: UUID
    class_ids: Sequence[UUID] | None = None
    subclass_ids: Sequence[UUID] | None = None
    name: str | None = None
    description: str | None = None
    next_level_description: str | None = None
    level: int | None = None
    school: str | None = None
    damage_type: SpellDamageTypeCommand | None = None
    duration: SpellDurationCommand | None = None
    casting_time: GameTimeCommand | None = None
    spell_range: LengthCommand | None = None
    splash: SplashCommand | None = None
    components: SpellComponentsCommand | None = None
    concentration: bool | None = None
    ritual: bool | None = None
    saving_throws: Sequence[str] | None = None
    name_in_english: str | None = None
    source_id: UUID | None = None

    def __post_init__(self):
        if all(
            [
                self.class_ids is None,
                self.subclass_ids is None,
                self.name is None,
                self.description is None,
                self.next_level_description is None,
                self.level is None,
                self.school is None,
                self.damage_type is None,
                self.duration is None,
                self.casting_time is None,
                self.spell_range is None,
                self.splash is None,
                self.components is None,
                self.concentration is None,
                self.ritual is None,
                self.saving_throws is None,
                self.name_in_english is None,
                self.source_id is None,
            ]
        ):
            raise DomainError.invalid_data(
                "не переданы данные для обновления заклинания"
            )


@dataclass
class DeleteSpellCommand:
    user_id: UUID
    spell_id: UUID
