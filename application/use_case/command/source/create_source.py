from uuid import UUID

from application.dto.command.source import CreateSourceCommand
from application.dto.model.source import AppSource
from application.repository import SourceRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.source import Source, SourceService


class CreateSourceUseCase(UserCheck):
    def __init__(
        self,
        source_service: SourceService,
        user_repository: UserRepository,
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._source_service = source_service
        self._source_repository = source_repository

    async def execute(self, command: CreateSourceCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self._source_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать источник с названием {command.name}"
            )
        source = Source(
            await self._source_repository.next_id(),
            command.name,
            command.description,
            command.name_in_english,
        )
        await self._source_repository.save(AppSource.from_domain(source))
        return source.source_id()
