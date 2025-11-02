from application.dto.command.character_class import CharacterClassUpdateCommand
from application.repository import (
    ClassRepository,
    ToolRepository,
    UserRepository,
    WeaponRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.armor.armor_type import ArmorType
from domain.character_class import ClassHits, ClassProficiencies, ClassService
from domain.dice import Dice
from domain.error import DomainError
from domain.modifier import Modifier
from domain.skill import Skill


class UpdateClassUseCase(UserCheck):
    def __init__(
        self,
        class_service: ClassService,
        user_repository: UserRepository,
        class_repository: ClassRepository,
        weapon_repository: WeaponRepository,
        tool_repository: ToolRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__class_service = class_service
        self.__class_repository = class_repository
        self.__weapon_repository = weapon_repository
        self.__tool_repository = tool_repository

    async def execute(self, command: CharacterClassUpdateCommand) -> None:
        self.__check_user(command.user_id)
        if not await self.__class_repository.is_class_of_id_exist(command.class_id):
            raise DomainError.not_found(f"класса с id {command.class_id} не существует")
        changing_class = await self.__class_repository.get_class_of_id(command.class_id)
        if command.name is not None:
            await self.__class_service.can_rename_with_name(command.name)
            changing_class.new_name(command.name)
        if command.description is not None:
            changing_class.new_description(command.description)
        if command.primary_modifiers is not None:
            changing_class.new_primary_modifiers(
                [Modifier.from_str(modifier) for modifier in command.primary_modifiers]
            )
        if command.hit_dice is not None:
            changing_class.new_hits(
                ClassHits(
                    Dice.from_str(command.hit_dice),
                    command.starting_hits,
                    Modifier.from_str(command.hit_modifier),
                    command.next_level_hits,
                )
            )
        if command.armors is not None:
            for weapon_id in command.weapon:
                if not await self.__weapon_repository.is_weapon_of_id_exist(weapon_id):
                    raise DomainError.invalid_data(
                        f"оружия с id {weapon_id} не существует"
                    )
            for tool_id in command.tools:
                if not await self.__tool_repository.is_tool_of_id_exist(tool_id):
                    raise DomainError.invalid_data(
                        f"инструментов с id {tool_id} не существует"
                    )
            changing_class.new_proficiencies(
                ClassProficiencies(
                    [ArmorType.from_str(armor) for armor in command.armors],
                    command.weapon,
                    command.tools,
                    [Modifier.from_str(modifier) for modifier in command.saving_throws],
                    [Skill.from_str(skill) for skill in command.skills],
                    command.number_skills,
                    command.number_tools,
                )
            )
        if command.name_in_english is not None:
            changing_class.new_name_in_english(command.name_in_english)
        await self.__class_repository.save(changing_class)
