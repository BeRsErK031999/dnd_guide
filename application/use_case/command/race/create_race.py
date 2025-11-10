from application.dto.command.race import CreateRaceCommand
from application.repository import (
    CreatureSizeRepository,
    CreatureTypeRepository,
    RaceRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.length import Length, LengthUnit
from domain.modifier import Modifier
from domain.race import (
    Race,
    RaceAge,
    RaceFeature,
    RaceIncreaseModifier,
    RaceService,
    RaceSpeed,
)


class CreateRaceUseCase(UserCheck):
    def __init__(
        self,
        race_service: RaceService,
        user_repository: UserRepository,
        race_repository: RaceRepository,
        creature_size_repository: CreatureSizeRepository,
        creature_type_repository: CreatureTypeRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__race_service = race_service
        self.__race_repository = race_repository
        self.__size_repository = creature_size_repository
        self.__type_repository = creature_type_repository

    async def execute(self, command: CreateRaceCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__race_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать расу с названием {command.name}"
            )
        if not await self.__size_repository.id_exists(command.size_id):
            raise DomainError.invalid_data(
                f"размера существ с id {command.size_id} не существует"
            )
        if not await self.__type_repository.id_exists(command.type_id):
            raise DomainError.invalid_data(
                f"типа существ с id {command.type_id} не существует"
            )
        race = Race(
            await self.__race_repository.next_id(),
            command.name,
            command.description,
            command.type_id,
            command.size_id,
            RaceSpeed(
                Length(
                    command.speed.base_speed.count,
                    LengthUnit.from_str(command.speed.base_speed.unit),
                ),
                command.speed.description,
            ),
            RaceAge(command.age.max_age, command.age.description),
            [
                RaceIncreaseModifier(
                    Modifier.from_str(increase_modifier.modifier),
                    increase_modifier.bonus,
                )
                for increase_modifier in command.increase_modifiers
            ],
            [
                RaceFeature(feature.name, feature.description)
                for feature in command.features
            ],
            command.name_in_english,
        )
        await self.__race_repository.save(race)
