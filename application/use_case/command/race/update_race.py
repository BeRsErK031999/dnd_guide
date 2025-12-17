from application.dto.command.race import UpdateRaceCommand
from application.dto.model.race import AppRace
from application.repository import RaceRepository, SourceRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.creature_size import CreatureSize
from domain.creature_type import CreatureType
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
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._race_service = race_service
        self._race_repository = race_repository
        self._source_repository = source_repository

    async def execute(self, command: UpdateRaceCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._race_repository.id_exists(command.race_id):
            raise DomainError.not_found(f"расы с id {command.race_id} не существует")
        app_race = await self._race_repository.get_by_id(command.race_id)
        race = app_race.to_domain()
        if command.name is not None:
            if not await self._race_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    "не возможно переименовать расу с использованием "
                    f"названия {command.name}"
                )
            race.new_name(command.name)
        if command.description is not None:
            race.new_description(command.description)
        if command.creature_size is not None:
            race.new_creature_size(CreatureSize.from_str(command.creature_size))
        if command.creature_type is not None:
            race.new_creature_type(CreatureType.from_str(command.creature_type))
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
            if not await self._source_repository.id_exists(command.source_id):
                raise DomainError.invalid_data(
                    f"источник с id {command.source_id} не существует"
                )
            race.new_source_id(command.source_id)
        await self._race_repository.save(AppRace.from_domain(race))
