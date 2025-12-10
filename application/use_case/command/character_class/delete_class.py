from application.dto.command.character_class import DeleteClassCommand
from application.repository import ClassRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteClassUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        class_repository: ClassRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._class_repository = class_repository

    async def execute(self, command: DeleteClassCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._class_repository.id_exists(command.class_id):
            raise DomainError.not_found(f"класса с id {command.class_id} не существует")
        await self._class_repository.delete(command.class_id)
