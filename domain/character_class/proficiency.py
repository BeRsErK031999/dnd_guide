from typing import Sequence
from uuid import UUID

from domain.armor.armor_type import ArmorType
from domain.error import DomainError
from domain.modifier import Modifier
from domain.skill import Skill


class ClassProficiencies:
    def __init__(
        self,
        armors: Sequence[ArmorType],
        weapons: Sequence[UUID],
        tools: Sequence[UUID],
        saving_throws: Sequence[Modifier],
        skills: Sequence[Skill],
        number_skills: int,
        number_tools: int = 1,
    ) -> None:
        self._validate_duplicate(armors, "типы доспехов содержат дубликаты")
        self._validate_duplicate(weapons, "оружия содержат дубликаты")
        self._validate_duplicate(tools, "инструменты содержат дубликаты")
        self._validate_duplicate(saving_throws, "спасброски содержат дубликаты")
        self._validate_duplicate(skills, "навыки содержат дубликаты")
        self._armors = list(armors)
        self._weapons = list(weapons)
        self._tools = list(tools)
        self._number_tools = number_tools
        self._saving_throws = list(saving_throws)
        self._skills = list(skills)
        self._number_skills = number_skills

    def armors(self) -> list[ArmorType]:
        return self._armors

    def weapons(self) -> list[UUID]:
        return self._weapons

    def tools(self) -> list[UUID]:
        return self._tools

    def number_tools(self) -> int:
        return self._number_tools

    def saving_throws(self) -> list[Modifier]:
        return self._saving_throws

    def skills(self) -> list[Skill]:
        return self._skills

    def number_skills(self) -> int:
        return self._number_skills

    def _validate_duplicate(self, seq: Sequence, msg: str) -> None:
        if len(seq) == 0:
            return
        if len(seq) != len(set(seq)):
            raise DomainError.invalid_data(msg)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._armors == value._armors
                and set(self._weapons) == set(value._weapons)
                and set(self._tools) == set(value._tools)
                and set(self._saving_throws) == set(value._saving_throws)
                and set(self._skills) == set(value._skills)
                and self._number_skills == value._number_skills
                and self._number_tools == value._number_tools
            )
        raise NotImplemented
