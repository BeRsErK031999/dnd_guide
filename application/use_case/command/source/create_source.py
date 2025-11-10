from application.dto.command.source import CreateSourceCommand
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
        self.__source_service = source_service
        self.__source_repository = source_repository

    async def execute(self, command: CreateSourceCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__source_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать источник с названием {command.name}"
            )
        source = Source(
            await self.__source_repository.next_id(),
            command.name,
            command.description,
            command.name_in_english,
        )
        await self.__source_repository.save(source)
