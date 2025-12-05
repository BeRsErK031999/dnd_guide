from application.dto.command.character_class import UpdateClassCommand
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
from domain.character_class import ClassHits, ClassProficiencies, ClassService
from domain.dice import Dice, DiceType
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
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__class_service = class_service
        self.__class_repository = class_repository
        self.__weapon_repository = weapon_repository
        self.__tool_repository = tool_repository
        self.__source_repository = source_repository

    async def execute(self, command: UpdateClassCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__class_repository.id_exists(command.class_id):
            raise DomainError.not_found(f"класса с id {command.class_id} не существует")
        app_changing_class = await self.__class_repository.get_by_id(command.class_id)
        changing_class = app_changing_class.to_domain()
        if command.name is not None:
            await self.__class_service.can_rename_with_name(command.name)
            changing_class.new_name(command.name)
        if command.description is not None:
            changing_class.new_description(command.description)
        if command.primary_modifiers is not None:
            changing_class.new_primary_modifiers(
                [Modifier.from_str(modifier) for modifier in command.primary_modifiers]
            )
        if command.hits is not None:
            changing_class.new_hits(
                ClassHits(
                    Dice(
                        command.hits.hit_dice.count,
                        DiceType.from_str(command.hits.hit_dice.dice_type),
                    ),
                    command.hits.starting_hits,
                    Modifier.from_str(command.hits.hit_modifier),
                    command.hits.next_level_hits,
                )
            )
        if command.proficiencies is not None:
            for weapon_id in command.proficiencies.weapons:
                if not await self.__weapon_repository.id_exists(weapon_id):
                    raise DomainError.invalid_data(
                        f"оружия с id {weapon_id} не существует"
                    )
            for tool_id in command.proficiencies.tools:
                if not await self.__tool_repository.id_exists(tool_id):
                    raise DomainError.invalid_data(
                        f"инструментов с id {tool_id} не существует"
                    )
            changing_class.new_proficiencies(
                ClassProficiencies(
                    [
                        ArmorType.from_str(armor)
                        for armor in command.proficiencies.armors
                    ],
                    command.proficiencies.weapons,
                    command.proficiencies.tools,
                    [
                        Modifier.from_str(modifier)
                        for modifier in command.proficiencies.saving_throws
                    ],
                    [Skill.from_str(skill) for skill in command.proficiencies.skills],
                    command.proficiencies.number_skills,
                    command.proficiencies.number_tools,
                )
            )
        if command.name_in_english is not None:
            changing_class.new_name_in_english(command.name_in_english)
        if command.source_id is not None:
            if not await self.__source_repository.id_exists(command.source_id):
                raise DomainError.invalid_data(
                    f"источник с id {command.source_id} не существует"
                )
            changing_class.new_source_id(command.source_id)
        await self.__class_repository.update(AppClass.from_domain(changing_class))
