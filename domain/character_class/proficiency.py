from domain.armor_type import ArmorType
from domain.character_class.skill import ClassSkill
from domain.modifier import Modifier
from domain.tool_type import ToolType
from domain.weapon_kind.weapon_type import WeaponType


class ClassProficiency:
    def __init__(
        self,
        armors: list[ArmorType],
        weapon: list[WeaponType],
        tools: list[ToolType],
        saving_throws: list[Modifier],
        skills: list[ClassSkill],
        number_skills: int,
        number_tools: int = 1,
    ) -> None:
        self.__armors = armors
        self.__weapon = weapon
        self.__tools = tools
        if len(tools) == 0:
            self.__number_tools = 0
        else:
            self.__number_tools = number_tools
        self.__saving_throws = saving_throws
        self.__skills = skills
        self.__number_skills = number_skills

    def armors(self) -> list[ArmorType]:
        return self.__armors

    def weapon(self) -> list[WeaponType]:
        return self.__weapon

    def tools(self) -> list[ToolType]:
        return self.__tools

    def number_tools(self) -> int:
        return self.__number_tools

    def saving_throws(self) -> list[Modifier]:
        return self.__saving_throws

    def skills(self) -> list[ClassSkill]:
        return self.__skills

    def number_skills(self) -> int:
        return self.__number_skills

    def __str__(self) -> str:
        return (
            f"доспехи: {self.__armors}\nоружие: {self.__weapon}\n"
            f"количество инструментов: {self.__number_tools}\nинструменты: {self.__tools}\n"
            f"спасброски: {self.__saving_throws}\n"
            f"количество навыков: {self.__number_skills}\nнавыки: {self.__skills}"
        )
