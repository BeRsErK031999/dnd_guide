from application.dto.command.race import UpdateRaceCommand
from application.repository import (
    CreatureSizeRepository,
    CreatureTypeRepository,
    RaceRepository,
    SourceRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.length import Length, LengthUnit
from domain.modifier import Modifier
from domain.race import (
    RaceAge,
    RaceFeature,
    RaceIncreaseModifier,
    RaceService,
    RaceSpeed,
)


class UpdateRaceUseCase(UserCheck):
    def __init__(
        self,
        race_service: RaceService,
        user_repository: UserRepository,
        race_repository: RaceRepository,
        creature_size_repository: CreatureSizeRepository,
        creature_type_repository: CreatureTypeRepository,
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__race_service = race_service
        self.__race_repository = race_repository
        self.__size_repository = creature_size_repository
        self.__type_repository = creature_type_repository
        self.__source_repository = source_repository

    async def execute(self, command: UpdateRaceCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__race_repository.id_exists(command.race_id):
            raise DomainError.not_found(f"расы с id {command.race_id} не существует")
        race = await self.__race_repository.get_by_id(command.race_id)
        if command.name is not None:
            if not await self.__race_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    "не возможно переименовать расу с использованием "
                    f"названия {command.name}"
                )
            race.new_name(command.name)
        if command.description is not None:
            race.new_description(command.description)
        if command.size_id is not None:
            if not await self.__size_repository.id_exists(command.size_id):
                raise DomainError.invalid_data(
                    f"размера существ с id {command.size_id} не существует"
                )
            race.new_size_id(command.size_id)
        if command.type_id is not None:
            if not await self.__type_repository.id_exists(command.type_id):
                raise DomainError.invalid_data(
                    f"типа существ с id {command.type_id} не существует"
                )
            race.new_type_id(command.type_id)
        if command.speed is not None:
            race.new_speed(
                RaceSpeed(
                    Length(
                        command.speed.base_speed.count,
                        LengthUnit.from_str(command.speed.base_speed.unit),
                    ),
                    command.speed.description,
                )
            )
        if command.age is not None:
            race.new_age(RaceAge(command.age.max_age, command.age.description))
        if command.increase_modifiers is not None:
            race.new_increase_modifiers(
                [
                    RaceIncreaseModifier(
                        Modifier.from_str(increase_modifier.modifier),
                        increase_modifier.bonus,
                    )
                    for increase_modifier in command.increase_modifiers
                ]
            )
        if command.new_features is not None:
            race.new_features(
                [
                    RaceFeature(feature.name, feature.description)
                    for feature in command.new_features
                ]
            )
        if command.add_features is not None:
            race.add_features(
                [
                    RaceFeature(feature.name, feature.description)
                    for feature in command.add_features
                ]
            )
        if command.remove_features is not None:
            race.remove_features(command.remove_features)
        if command.name_in_english is not None:
            race.new_name_in_english(command.name_in_english)
        if command.source_id is not None:
            if not await self.__source_repository.id_exists(command.source_id):
                raise DomainError.invalid_data(
                    f"источник с id {command.source_id} не существует"
                )
            race.new_source_id(command.source_id)
        await self.__race_repository.update(race)
