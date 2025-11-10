from application.dto.command.character_class import CreateClassCommand
from application.repository import (
    ClassRepository,
    ToolRepository,
    UserRepository,
    WeaponRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.armor import ArmorType
from domain.character_class import (
    CharacterClass,
    ClassHits,
    ClassProficiencies,
    ClassService,
)
from domain.dice import Dice, DiceType
from domain.error import DomainError
from domain.modifier import Modifier
from domain.skill import Skill


class CreateClassUseCase(UserCheck):
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

    async def execute(self, command: CreateClassCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__class_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"класс с названием {command.name} уже существует"
            )
        for weapon_id in command.proficiencies.weapon:
            if not await self.__weapon_repository.id_exists(weapon_id):
                raise DomainError.invalid_data(f"оружия с id {weapon_id} не существует")
        for tool_id in command.proficiencies.tools:
            if not await self.__tool_repository.id_exists(tool_id):
                raise DomainError.invalid_data(
                    f"инструментов с id {tool_id} не существует"
                )
        new_class = CharacterClass(
            await self.__class_repository.next_id(),
            command.name,
            command.description,
            [Modifier.from_str(modifier) for modifier in command.primary_modifiers],
            ClassHits(
                Dice(
                    command.hits.hit_dice.count,
                    DiceType.from_str(command.hits.hit_dice.dice_type),
                ),
                command.hits.starting_hits,
                Modifier.from_str(command.hits.hit_modifier),
                command.hits.next_level_hits,
            ),
            ClassProficiencies(
                [
                    ArmorType.from_str(armor_type)
                    for armor_type in command.proficiencies.armors
                ],
                command.proficiencies.weapon,
                command.proficiencies.tools,
                [
                    Modifier.from_str(saving_throw)
                    for saving_throw in command.proficiencies.saving_throws
                ],
                [Skill.from_str(skill) for skill in command.proficiencies.skills],
                command.proficiencies.number_skills,
                command.proficiencies.number_tools,
            ),
            command.name_in_english,
        )
        await self.__class_repository.save(new_class)
