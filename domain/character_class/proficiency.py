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
        self.__validate_duplicate(armors, "типы доспехов содержат дубликаты")
        self.__validate_duplicate(weapons, "оружия содержат дубликаты")
        self.__validate_duplicate(tools, "инструменты содержат дубликаты")
        self.__validate_duplicate(saving_throws, "спасброски содержат дубликаты")
        self.__validate_duplicate(skills, "навыки содержат дубликаты")
        self.__armors = list(armors)
        self.__weapons = list(weapons)
        self.__tools = list(tools)
        self.__number_tools = number_tools
        self.__saving_throws = list(saving_throws)
        self.__skills = list(skills)
        self.__number_skills = number_skills

    def armors(self) -> list[ArmorType]:
        return self.__armors

    def weapons(self) -> list[UUID]:
        return self.__weapons

    def tools(self) -> list[UUID]:
        return self.__tools

    def number_tools(self) -> int:
        return self.__number_tools

    def saving_throws(self) -> list[Modifier]:
        return self.__saving_throws

    def skills(self) -> list[Skill]:
        return self.__skills

    def number_skills(self) -> int:
        return self.__number_skills

    def __validate_duplicate(self, seq: Sequence, msg: str) -> None:
        if len(seq) == 0:
            return
        if len(seq) != len(set(seq)):
            raise DomainError.invalid_data(msg)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__armors == value.__armors
                and set(self.__weapons) == set(value.__weapons)
                and set(self.__tools) == set(value.__tools)
                and set(self.__saving_throws) == set(value.__saving_throws)
                and set(self.__skills) == set(value.__skills)
                and self.__number_skills == value.__number_skills
                and self.__number_tools == value.__number_tools
            )
        raise NotImplemented
