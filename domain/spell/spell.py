from typing import Sequence
from uuid import UUID

from domain.damage_type import DamageType
from domain.error import DomainError
from domain.game_time import GameTime
from domain.length import Length
from domain.mixin import EntityDescription, EntityName, EntityNameInEnglish
from domain.modifier import Modifier
from domain.spell.components import SpellComponents
from domain.spell.school import SpellSchool


class Spell(EntityName, EntityNameInEnglish, EntityDescription):
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
        components: SpellComponents,
        concentration: bool,
        ritual: bool,
        saving_throws: Sequence[Modifier],
        name_in_english: str,
    ) -> None:
        self.__validate_class_ids(class_ids)
        self.__validate_level(level)
        self.__validate_duplicate_in_seq(
            subclass_ids, "список подклассов содержит дубликаты"
        )
        self.__validate_duplicate_in_seq(
            saving_throws, "спасброски заклинания содержат дубликаты"
        )
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        EntityNameInEnglish.__init__(self, name_in_english)
        self.__spell_id = spell_id
        self.__class_ids = list(class_ids)
        self.__subclass_ids = list(subclass_ids)
        self.__next_level_description = next_level_description
        self.__level = level
        self.__school = school
        self.__damage_type = damage_type
        self.__duration = duration
        self.__casting_time = casting_time
        self.__spell_range = spell_range
        self.__components = components
        self.__concentration = concentration
        self.__ritual = ritual
        self.__saving_throws = list(saving_throws)

    def spell_id(self) -> UUID:
        return self.__spell_id

    def class_ids(self) -> list[UUID]:
        return self.__class_ids

    def subclass_ids(self) -> list[UUID]:
        return self.__subclass_ids

    def next_level_description(self) -> str:
        return self.__next_level_description

    def level(self) -> int:
        return self.__level

    def school(self) -> SpellSchool:
        return self.__school

    def damage_type(self) -> DamageType | None:
        return self.__damage_type

    def duration(self) -> GameTime | None:
        return self.__duration

    def casting_time(self) -> GameTime:
        return self.__casting_time

    def spell_range(self) -> Length:
        return self.__spell_range

    def components(self) -> SpellComponents:
        return self.__components

    def concentration(self) -> bool:
        return self.__concentration

    def ritual(self) -> bool:
        return self.__ritual

    def saving_throws(self) -> list[Modifier]:
        return self.__saving_throws

    def new_class_ids(self, class_ids: list[UUID]) -> None:
        if set(self.__class_ids) == set(class_ids):
            raise DomainError.idempotent(
                "текущий список классов равен новому списку классов"
            )
        self.__validate_class_ids(class_ids)
        self.__class_ids = class_ids

    def new_subclass_ids(self, subclass_ids: list[UUID]) -> None:
        if set(self.__subclass_ids) == set(subclass_ids):
            raise DomainError.idempotent(
                "текущий список подклассов равен новому списку подклассов"
            )
        self.__validate_duplicate_in_seq(
            subclass_ids, "список подклассов содержит дубликаты"
        )
        self.__subclass_ids = subclass_ids

    def new_next_level_description(self, description: str) -> None:
        self.__next_level_description = description

    def new_level(self, level: int) -> None:
        if self.__level == level:
            raise DomainError.idempotent("текущий уровень равен новому уровню")
        self.__validate_level(level)
        self.__level = level

    def new_school(self, school: SpellSchool) -> None:
        if self.__school == school:
            raise DomainError.idempotent("текущая школа равна новой школе")
        self.__school = school

    def new_damage_type(self, damage_type: DamageType | None) -> None:
        if self.__damage_type == damage_type:
            raise DomainError.idempotent("текущий урон равен новому урону")
        self.__damage_type = damage_type

    def new_duration(self, duration: GameTime | None) -> None:
        if self.__duration == duration:
            raise DomainError.idempotent(
                "текущая длительность равна новой длительности"
            )
        self.__duration = duration

    def new_casting_time(self, casting_time: GameTime) -> None:
        if self.__casting_time == casting_time:
            raise DomainError.idempotent(
                "текущее время каста равно новому времени каста"
            )
        self.__casting_time = casting_time

    def new_spell_range(self, spell_range: Length) -> None:
        if self.__spell_range == spell_range:
            raise DomainError.idempotent("текущий радиус равен новому радиусу")
        self.__spell_range = spell_range

    def new_components(self, components: SpellComponents) -> None:
        if self.__components == components:
            raise DomainError.idempotent(
                "текущий набор компонентов равен новому набору компонентов"
            )
        self.__components = components

    def new_concentration(self, concentration: bool) -> None:
        if self.__concentration == concentration:
            raise DomainError.idempotent(
                "текущая концентрация равна новой концентрации"
            )
        self.__concentration = concentration

    def new_ritual(self, ritual: bool) -> None:
        if self.__ritual == ritual:
            raise DomainError.idempotent("текущий ритуал равен новому ритуалу")
        self.__ritual = ritual

    def new_saving_throws(self, saving_throws: Sequence[Modifier]) -> None:
        if set(self.__saving_throws) == set(saving_throws):
            raise DomainError.idempotent(
                "текущий набор спасбросков равен новому набору спасбросков"
            )
        self.__validate_duplicate_in_seq(
            saving_throws, "набор спасбросков содержит дубликаты"
        )
        self.__saving_throws = list(saving_throws)

    def __validate_class_ids(self, class_ids: Sequence[UUID]) -> None:
        if len(class_ids) == 0:
            raise DomainError.invalid_data(
                "у заклинания должен быть хотя бы один класс, который "
                "может его использовать"
            )
        if len(class_ids) != len(set(class_ids)):
            raise DomainError.invalid_data("список классов содержит дубликаты")

    def __validate_duplicate_in_seq(self, seq: Sequence, msg: str) -> None:
        if len(seq) != len(set(seq)):
            raise DomainError.invalid_data(msg)

    def __validate_level(self, level: int) -> None:
        if level < 0 or level > 9:
            raise DomainError.invalid_data(
                "уровень заклинания должен находиться в диапазоне от 0 до 9"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__spell_id == value.__spell_id
        if isinstance(value, UUID):
            return self.__spell_id == value
        raise NotImplemented
