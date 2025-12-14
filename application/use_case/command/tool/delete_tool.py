from application.dto.command.tool import DeleteToolCommand
from application.repository import ClassRepository, ToolRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteToolUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        tool_repository: ToolRepository,
        class_repository: ClassRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._tool_repository = tool_repository
        self._class_repository = class_repository

    async def execute(self, command: DeleteToolCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._tool_repository.id_exists(command.tool_id):
            raise DomainError.not_found(
                f"инструмент с id {command.tool_id} не существует"
            )
        exists_classes = await self._class_repository.filter(
            filter_by_tool_ids=[command.tool_id]
        )
        if len(exists_classes) > 0:
            raise DomainError.invalid_data(
                "инструменты используются для классов: "
                f"{", ".join(c.name for c in exists_classes)}"
            )
        await self._tool_repository.delete(command.tool_id)
