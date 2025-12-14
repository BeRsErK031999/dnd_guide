from uuid import UUID

from application.dto.command.subrace import CreateSubraceCommand
from application.dto.model.subrace import AppSubrace
from application.repository import RaceRepository, UserRepository
from application.repository.subrace import SubraceRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.modifier import Modifier
from domain.subrace.feature import SubraceFeature
from domain.subrace.increase_modifier import SubraceIncreaseModifier
from domain.subrace.service import SubraceService
from domain.subrace.subrace import Subrace


class CreateSubraceUseCase(UserCheck):
    def __init__(
        self,
        subrace_service: SubraceService,
        user_repository: UserRepository,
        subrace_repository: SubraceRepository,
        race_repository: RaceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._subrace_service = subrace_service
        self._subrace_repository = subrace_repository
        self._race_repository = race_repository

    async def execute(self, command: CreateSubraceCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self._subrace_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать подрасу с названием {command.name}"
            )
        if not await self._race_repository.id_exists(command.race_id):
            raise DomainError.invalid_data(f"расы с id {command.race_id} не существует")
        subrace = Subrace(
            await self._subrace_repository.next_id(),
            command.race_id,
            command.name,
            command.description,
            [
                SubraceIncreaseModifier(
                    Modifier.from_str(increase_modifier.modifier),
                    increase_modifier.bonus,
                )
                for increase_modifier in command.increase_modifiers
            ],
            [
                SubraceFeature(feature.name, feature.description)
                for feature in command.features
            ],
            command.name_in_english,
        )
        await self._subrace_repository.create(AppSubrace.from_domain(subrace))
        return subrace.subrace_id()
