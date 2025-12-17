from application.dto.command.subrace import UpdateSubraceCommand
from application.dto.model.subrace import AppSubrace
from application.repository import RaceRepository, SubraceRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.modifier import Modifier
from domain.subrace import SubraceFeature, SubraceIncreaseModifier, SubraceService


class UpdateSubraceUseCase(UserCheck):
    def __init__(
        self,
        subrace_service: SubraceService,
        user_repository: UserRepository,
        subrace_repository: SubraceRepository,
        race_repository: RaceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._subrace_service = subrace_service
        self._race_repository = race_repository
        self._subrace_repository = subrace_repository

    async def execute(self, command: UpdateSubraceCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._subrace_repository.id_exists(command.subrace_id):
            raise DomainError.not_found(f"подрасы с id {command.race_id} не существует")
        app_subrace = await self._subrace_repository.get_by_id(command.subrace_id)
        subrace = app_subrace.to_domain()
        if command.race_id is not None:
            if not await self._race_repository.id_exists(command.race_id):
                raise DomainError.invalid_data(f"расы с id {command} не существует")
            subrace.new_race_id(command.race_id)
        if command.name is not None:
            if not await self._subrace_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    "не возможно переименовать подрасу с использованием "
                    f"названия {command.name}"
                )
            subrace.new_name(command.name)
        if command.description is not None:
            subrace.new_description(command.description)
        if command.increase_modifiers is not None:
            subrace.new_increase_modifiers(
                [
                    SubraceIncreaseModifier(
                        Modifier.from_str(increase_modifier.modifier),
                        increase_modifier.bonus,
                    )
                    for increase_modifier in command.increase_modifiers
                ]
            )
        if command.new_features is not None:
            subrace.new_features(
                [
                    SubraceFeature(feature.name, feature.description)
                    for feature in command.new_features
                ]
            )
        if command.add_features is not None:
            subrace.add_features(
                [
                    SubraceFeature(feature.name, feature.description)
                    for feature in command.add_features
                ]
            )
        if command.remove_features is not None:
            subrace.remove_features(command.remove_features)
        if command.name_in_english is not None:
            subrace.new_name_in_english(command.name_in_english)
        await self._subrace_repository.save(AppSubrace.from_domain(subrace))
