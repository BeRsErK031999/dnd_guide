from application.dto.command.spell import CreateSpellCommand
from application.repository import (
    ClassRepository,
    SourceRepository,
    SpellRepository,
    SubclassRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.damage_type import DamageType
from domain.error import DomainError
from domain.game_time import GameTime, GameTimeUnit
from domain.length import Length, LengthUnit
from domain.modifier import Modifier
from domain.spell import Spell, SpellComponents, SpellSchool, SpellService


class CreateSpellUseCase(UserCheck):
    def __init__(
        self,
        spell_service: SpellService,
        user_repository: UserRepository,
        spell_repository: SpellRepository,
        class_repository: ClassRepository,
        subclass_repository: SubclassRepository,
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__spell_service = spell_service
        self.__spell_repository = spell_repository
        self.__class_repository = class_repository
        self.__subclass_repository = subclass_repository
        self.__source_repository = source_repository

    async def execute(self, command: CreateSpellCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__spell_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"заклинание с именем {command.name} не возможно создать"
            )
        for class_id in command.class_ids:
            if not await self.__class_repository.id_exists(class_id):
                raise DomainError.invalid_data(f"класс с id {class_id} не существует")
        for subclass_id in command.subclass_ids:
            if not await self.__subclass_repository.id_exists(subclass_id):
                raise DomainError.invalid_data(
                    f"подкласс с id {subclass_id} не существует"
                )
        if not await self.__source_repository.id_exists(command.source_id):
            raise DomainError.invalid_data(
                f"источник с id {command.source_id} не существует"
            )
        spell = Spell(
            await self.__spell_repository.next_id(),
            command.class_ids,
            command.subclass_ids,
            command.name,
            command.description,
            command.next_level_description,
            command.level,
            SpellSchool.from_str(command.school),
            (
                DamageType.from_str(command.damage_type.name)
                if command.damage_type is not None
                and command.damage_type.name is not None
                else None
            ),
            (
                GameTime(
                    command.duration.game_time.count,
                    GameTimeUnit.from_str(command.duration.game_time.unit),
                )
                if command.duration is not None
                and command.duration.game_time is not None
                else None
            ),
            GameTime(
                command.casting_time.count,
                GameTimeUnit.from_str(command.casting_time.unit),
            ),
            Length(
                command.spell_range.count, LengthUnit.from_str(command.spell_range.unit)
            ),
            SpellComponents(
                command.components.verbal,
                command.components.symbolic,
                command.components.material,
                command.components.materials,
            ),
            command.concentration,
            command.ritual,
            [Modifier.from_str(modifier) for modifier in command.saving_throws],
            command.name_in_english,
            command.source_id,
        )
        await self.__spell_repository.create(spell)
