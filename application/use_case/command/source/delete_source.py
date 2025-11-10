from application.dto.command.source import DeleteSourceCommand
from application.repository import SourceRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteSourceUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        source_repository: SourceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__source_repository = source_repository

    async def execute(self, command: DeleteSourceCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__source_repository.id_exists(command.source_id):
            raise DomainError.not_found(
                f"источника с id {command.source_id} не существует"
            )
        await self.__source_repository.delete(command.source_id)
