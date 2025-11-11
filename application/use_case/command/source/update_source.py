from application.dto.command.source import UpdateSourceCommand
from application.repository import SourceRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.source import SourceService


class UpdateSourceUseCase(UserCheck):
    def __init__(
        self,
        source_service: SourceService,
        user_repository: UserRepository,
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__source_service = source_service
        self.__source_repository = source_repository

    async def execute(self, command: UpdateSourceCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__source_repository.id_exists(command.source_id):
            raise DomainError.not_found(
                f"источника с id {command.source_id} не существует"
            )
        source = await self.__source_repository.get_by_id(command.source_id)
        if command.name is not None:
            if not await self.__source_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"не возможно переименовать источник используя название {command.name}"
                )
            source.new_name(command.name)
        if command.description is not None:
            source.new_description(command.description)
        if command.name_in_english is not None:
            source.new_name_in_english(command.name_in_english)
        await self.__source_repository.update(source)
