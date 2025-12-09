from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.damage_type import DamageType
from domain.modifier import Modifier
from domain.spell import Spell, SpellComponents, SpellSchool

from .game_time import AppGameTime
from .length import AppLength

__all__ = [
    "AppSpell",
    "AppSpellComponents",
    "AppSpellSchool",
]


@dataclass
class AppSpellComponents:
    verbal: bool
    symbolic: bool
    material: bool
    materials: list[UUID]

    @staticmethod
    def from_domain(components: SpellComponents) -> "AppSpellComponents":
        return AppSpellComponents(
            verbal=components.verbal(),
            symbolic=components.symbolic(),
            material=components.material(),
            materials=components.materials(),
        )

    def to_domain(self) -> SpellComponents:
        return SpellComponents(
            verbal=self.verbal,
            symbolic=self.symbolic,
            material=self.material,
            materials=self.materials,
        )


@dataclass
class AppSpellSchool:
    abjuration: str
    conjuration: str
    divination: str
    enchantment: str
    evocation: str
    illusion: str
    necromancy: str
    transmutation: str

    @staticmethod
    def from_domain() -> "AppSpellSchool":
        return AppSpellSchool(
            **{school.name.lower(): school.value for school in SpellSchool}
        )


@dataclass
class AppSpell:
    spell_id: UUID
    class_ids: Sequence[UUID]
    subclass_ids: Sequence[UUID]
    name: str
    description: str
    next_level_description: str
    level: int
    school: str
    damage_type: str | None
    duration: AppGameTime | None
    casting_time: AppGameTime
    spell_range: AppLength
    splash: AppLength | None
    components: AppSpellComponents
    concentration: bool
    ritual: bool
    saving_throws: Sequence[str]
    name_in_english: str
    source_id: UUID

    @staticmethod
    def from_domain(spell: Spell) -> "AppSpell":
        damage_type = spell.damage_type()
        duration = spell.duration()
        splash = spell.splash()
        return AppSpell(
            spell_id=spell.spell_id(),
            class_ids=spell.class_ids(),
            subclass_ids=spell.subclass_ids(),
            name=spell.name(),
            description=spell.description(),
            next_level_description=spell.next_level_description(),
            level=spell.level(),
            school=spell.school().value,
            damage_type=(
                DamageType.from_str(damage_type) if damage_type is not None else None
            ),
            duration=(
                AppGameTime.from_domain(duration) if duration is not None else None
            ),
            casting_time=AppGameTime.from_domain(spell.casting_time()),
            spell_range=AppLength.from_domain(spell.spell_range()),
            splash=AppLength.from_domain(splash) if splash is not None else None,
            components=AppSpellComponents.from_domain(spell.components()),
            concentration=spell.concentration(),
            ritual=spell.ritual(),
            saving_throws=spell.saving_throws(),
            name_in_english=spell.name_in_english(),
            source_id=spell.source_id(),
        )

    def to_domain(self) -> Spell:
        return Spell(
            spell_id=self.spell_id,
            class_ids=self.class_ids,
            subclass_ids=self.subclass_ids,
            name=self.name,
            description=self.description,
            next_level_description=self.next_level_description,
            level=self.level,
            school=SpellSchool.from_str(self.school),
            damage_type=(
                DamageType.from_str(self.damage_type)
                if self.damage_type is not None
                else None
            ),
            duration=self.duration.to_domain() if self.duration is not None else None,
            casting_time=self.casting_time.to_domain(),
            spell_range=self.spell_range.to_domain(),
            splash=self.splash.to_domain() if self.splash is not None else None,
            components=self.components.to_domain(),
            concentration=self.concentration,
            ritual=self.ritual,
            saving_throws=[Modifier.from_str(m) for m in self.saving_throws],
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )
