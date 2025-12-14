from uuid import UUID

from application.dto.command.race import CreateRaceCommand
from application.dto.model.race import AppRace
from application.repository import RaceRepository, SourceRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.creature_size import CreatureSize
from domain.creature_type import CreatureType
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
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._race_service = race_service
        self._race_repository = race_repository
        self._source_repository = source_repository

    async def execute(self, command: CreateRaceCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self._race_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать расу с названием {command.name}"
            )
        if not await self._source_repository.id_exists(command.source_id):
            raise DomainError.invalid_data(
                f"источник с id {command.source_id} не существует"
            )
        race = Race(
            race_id=await self._race_repository.next_id(),
            name=command.name,
            description=command.description,
            creature_type=CreatureType.from_str(command.creature_type),
            creature_size=CreatureSize.from_str(command.creature_size),
            speed=RaceSpeed(
                Length(
                    command.speed.base_speed.count,
                    LengthUnit.from_str(command.speed.base_speed.unit),
                ),
                command.speed.description,
            ),
            age=RaceAge(command.age.max_age, command.age.description),
            increase_modifiers=[
                RaceIncreaseModifier(
                    Modifier.from_str(increase_modifier.modifier),
                    increase_modifier.bonus,
                )
                for increase_modifier in command.increase_modifiers
            ],
            features=[
                RaceFeature(feature.name, feature.description)
                for feature in command.features
            ],
            name_in_english=command.name_in_english,
            source_id=command.source_id,
        )
        await self._race_repository.create(AppRace.from_domain(race))
        return race.race_id()
