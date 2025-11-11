from application.dto.command.spell import UpdateSpellCommand
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
from domain.spell import SpellComponents, SpellSchool, SpellService


class UpdateSpellUseCase(UserCheck):
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

    async def execute(self, command: UpdateSpellCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__spell_repository.id_exists(command.spell_id):
            raise DomainError.not_found(
                f"заклинание с id {command.spell_id} не существует"
            )
        spell = await self.__spell_repository.get_by_id(command.spell_id)
        if command.class_ids is not None:
            for class_id in command.class_ids:
                if not await self.__class_repository.id_exists(class_id):
                    raise DomainError.invalid_data(
                        f"класс с id {class_id} не существует"
                    )
            spell.new_class_ids(command.class_ids)
        if command.subclass_ids is not None:
            for subclass_id in command.subclass_ids:
                if not await self.__subclass_repository.id_exists(subclass_id):
                    raise DomainError.invalid_data(
                        f"подкласс с id {subclass_id} не существует"
                    )
            spell.new_subclass_ids(command.subclass_ids)
        if command.name is not None:
            if not await self.__spell_service.can_create_with_name(command.name):
                raise DomainError.invalid_data(
                    f"заклинание не возможно переименовать с названием {command.name}"
                )
            spell.new_name(command.name)
        if command.description is not None:
            spell.new_description(command.description)
        if command.next_level_description is not None:
            spell.new_next_level_description(command.next_level_description)
        if command.level is not None:
            spell.new_level(command.level)
        if command.school is not None:
            spell.new_school(SpellSchool.from_str(command.school))
        if command.damage_type is not None:
            spell.new_damage_type(
                DamageType.from_str(command.damage_type.name)
                if command.damage_type is not None
                and command.damage_type.name is not None
                else None
            )
        if command.duration is not None:
            spell.new_duration(
                GameTime(
                    command.duration.game_time.count,
                    GameTimeUnit.from_str(command.duration.game_time.unit),
                )
                if command.duration is not None
                and command.duration.game_time is not None
                else None
            )
        if command.casting_time is not None:
            spell.new_casting_time(
                GameTime(
                    command.casting_time.count,
                    GameTimeUnit.from_str(command.casting_time.unit),
                )
            )
        if command.spell_range is not None:
            spell.new_spell_range(
                Length(
                    command.spell_range.count,
                    LengthUnit.from_str(command.spell_range.unit),
                )
            )
        if command.components is not None:
            spell.new_components(
                SpellComponents(
                    command.components.verbal,
                    command.components.symbolic,
                    command.components.material,
                    command.components.materials,
                )
            )
        if command.concentration is not None:
            spell.new_concentration(command.concentration)
        if command.ritual is not None:
            spell.new_ritual(command.ritual)
        if command.saving_throws is not None:
            spell.new_saving_throws(
                [Modifier.from_str(modifier) for modifier in command.saving_throws]
            )
        if command.name_in_english is not None:
            spell.new_name_in_english(command.name_in_english)
        if command.source_id is not None:
            if not await self.__source_repository.id_exists(command.source_id):
                raise DomainError.invalid_data(
                    f"источник с id {command.source_id} не существует"
                )
            spell.new_source_id(command.source_id)
        await self.__spell_repository.save(spell)
