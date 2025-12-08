from typing import Sequence
from uuid import UUID

from domain.damage_type import DamageType
from domain.error import DomainError
from domain.game_time import GameTime
from domain.length import Length
from domain.mixin import (
    EntityDescription,
    EntityName,
    EntityNameInEnglish,
    EntitySource,
)
from domain.modifier import Modifier
from domain.spell.components import SpellComponents
from domain.spell.school import SpellSchool


class Spell(EntityName, EntityNameInEnglish, EntityDescription, EntitySource):
    def __init__(
        self,
        spell_id: UUID,
        class_ids: Sequence[UUID],
        subclass_ids: Sequence[UUID],
        name: str,
        description: str,
        next_level_description: str,
        level: int,
        school: SpellSchool,
        damage_type: DamageType | None,
        duration: GameTime | None,
        casting_time: GameTime,
        spell_range: Length,
        splash: Length | None,
        components: SpellComponents,
        concentration: bool,
        ritual: bool,
        saving_throws: Sequence[Modifier],
        name_in_english: str,
        source_id: UUID,
    ) -> None:
        self._validate_class_ids(class_ids)
        self._validate_level(level)
        self._validate_duplicate_in_seq(
            subclass_ids, "список подклассов содержит дубликаты"
        )
        self._validate_duplicate_in_seq(
            saving_throws, "спасброски заклинания содержат дубликаты"
        )
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        EntityNameInEnglish.__init__(self, name_in_english)
        EntitySource.__init__(self, source_id)
        self._spell_id = spell_id
        self._class_ids = list(class_ids)
        self._subclass_ids = list(subclass_ids)
        self._next_level_description = next_level_description
        self._level = level
        self._school = school
        self._damage_type = damage_type
        self._duration = duration
        self._casting_time = casting_time
        self._spell_range = spell_range
        self._splash = splash
        self._components = components
        self._concentration = concentration
        self._ritual = ritual
        self._saving_throws = list(saving_throws)

    def spell_id(self) -> UUID:
        return self._spell_id

    def class_ids(self) -> list[UUID]:
        return self._class_ids

    def subclass_ids(self) -> list[UUID]:
        return self._subclass_ids

    def next_level_description(self) -> str:
        return self._next_level_description

    def level(self) -> int:
        return self._level

    def school(self) -> SpellSchool:
        return self._school

    def damage_type(self) -> DamageType | None:
        return self._damage_type

    def duration(self) -> GameTime | None:
        return self._duration

    def casting_time(self) -> GameTime:
        return self._casting_time

    def spell_range(self) -> Length:
        return self._spell_range

    def splash(self) -> Length | None:
        return self._splash

    def components(self) -> SpellComponents:
        return self._components

    def concentration(self) -> bool:
        return self._concentration

    def ritual(self) -> bool:
        return self._ritual

    def saving_throws(self) -> list[Modifier]:
        return self._saving_throws

    def new_class_ids(self, class_ids: Sequence[UUID]) -> None:
        if set(self._class_ids) == set(class_ids):
            raise DomainError.idempotent(
                "текущий список классов равен новому списку классов"
            )
        self._validate_class_ids(class_ids)
        self._class_ids = list(class_ids)

    def new_subclass_ids(self, subclass_ids: Sequence[UUID]) -> None:
        if set(self._subclass_ids) == set(subclass_ids):
            raise DomainError.idempotent(
                "текущий список подклассов равен новому списку подклассов"
            )
        self._validate_duplicate_in_seq(
            subclass_ids, "список подклассов содержит дубликаты"
        )
        self._subclass_ids = list(subclass_ids)

    def new_next_level_description(self, description: str) -> None:
        self._next_level_description = description

    def new_level(self, level: int) -> None:
        if self._level == level:
            raise DomainError.idempotent("текущий уровень равен новому уровню")
        self._validate_level(level)
        self._level = level

    def new_school(self, school: SpellSchool) -> None:
        if self._school == school:
            raise DomainError.idempotent("текущая школа равна новой школе")
        self._school = school

    def new_damage_type(self, damage_type: DamageType | None) -> None:
        if self._damage_type == damage_type:
            raise DomainError.idempotent("текущий урон равен новому урону")
        self._damage_type = damage_type

    def new_duration(self, duration: GameTime | None) -> None:
        if self._duration == duration:
            raise DomainError.idempotent(
                "текущая длительность равна новой длительности"
            )
        self._duration = duration

    def new_casting_time(self, casting_time: GameTime) -> None:
        if self._casting_time == casting_time:
            raise DomainError.idempotent(
                "текущее время каста равно новому времени каста"
            )
        self._casting_time = casting_time

    def new_spell_range(self, spell_range: Length) -> None:
        if self._spell_range == spell_range:
            raise DomainError.idempotent("текущий радиус равен новому радиусу")
        self._spell_range = spell_range

    def new_splash(self, splash: Length | None) -> None:
        if self._splash == splash:
            raise DomainError.idempotent("текущий сплеш равен новому")
        self._splash = splash

    def new_components(self, components: SpellComponents) -> None:
        if self._components == components:
            raise DomainError.idempotent(
                "текущий набор компонентов равен новому набору компонентов"
            )
        self._components = components

    def new_concentration(self, concentration: bool) -> None:
        if self._concentration == concentration:
            raise DomainError.idempotent(
                "текущая концентрация равна новой концентрации"
            )
        self._concentration = concentration

    def new_ritual(self, ritual: bool) -> None:
        if self._ritual == ritual:
            raise DomainError.idempotent("текущий ритуал равен новому ритуалу")
        self._ritual = ritual

    def new_saving_throws(self, saving_throws: Sequence[Modifier]) -> None:
        if set(self._saving_throws) == set(saving_throws):
            raise DomainError.idempotent(
                "текущий набор спасбросков равен новому набору спасбросков"
            )
        self._validate_duplicate_in_seq(
            saving_throws, "набор спасбросков содержит дубликаты"
        )
        self._saving_throws = list(saving_throws)

    def _validate_class_ids(self, class_ids: Sequence[UUID]) -> None:
        if len(class_ids) == 0:
            raise DomainError.invalid_data(
                "у заклинания должен быть хотя бы один класс, который "
                "может его использовать"
            )
        if len(class_ids) != len(set(class_ids)):
            raise DomainError.invalid_data("список классов содержит дубликаты")

    def _validate_duplicate_in_seq(self, seq: Sequence, msg: str) -> None:
        if len(seq) != len(set(seq)):
            raise DomainError.invalid_data(msg)

    def _validate_level(self, level: int) -> None:
        if level < 0 or level > 9:
            raise DomainError.invalid_data(
                "уровень заклинания должен находиться в диапазоне от 0 до 9"
            )

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._spell_id == value._spell_id
        if isinstance(value, UUID):
            return self._spell_id == value
        raise NotImplemented
