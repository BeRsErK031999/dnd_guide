from uuid import UUID

from application.dto.command.character_class import CreateClassCommand
from application.dto.model.character_class import AppClass
from application.repository import (
    ClassRepository,
    SourceRepository,
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
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._class_service = class_service
        self._class_repository = class_repository
        self._weapon_repository = weapon_repository
        self._tool_repository = tool_repository
        self._source_repository = source_repository

    async def execute(self, command: CreateClassCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self._class_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"класс с названием {command.name} уже существует"
            )
        for weapon_id in command.proficiencies.weapons:
            if not await self._weapon_repository.id_exists(weapon_id):
                raise DomainError.invalid_data(f"оружия с id {weapon_id} не существует")
        for tool_id in command.proficiencies.tools:
            if not await self._tool_repository.id_exists(tool_id):
                raise DomainError.invalid_data(
                    f"инструментов с id {tool_id} не существует"
                )
        if not await self._source_repository.id_exists(command.source_id):
            raise DomainError.invalid_data(
                f"источник с id {command.source_id} не существует"
            )
        new_class = CharacterClass(
            await self._class_repository.next_id(),
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
                command.proficiencies.weapons,
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
            command.source_id,
        )
        await self._class_repository.create(AppClass.from_domain(new_class))
        return new_class.class_id()
