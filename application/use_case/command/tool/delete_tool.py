from application.dto.command.tool import DeleteToolCommand
from application.repository import ToolRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteToolUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        tool_repository: ToolRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__tool_repository = tool_repository

    async def execute(self, command: DeleteToolCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__tool_repository.id_exists(command.tool_id):
            raise DomainError.not_found(
                f"инструмент с id {command.tool_id} не существует"
            )
        await self.__tool_repository.delete(command.tool_id)
