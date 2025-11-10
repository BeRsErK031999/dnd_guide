from application.dto.command.class_level import DeleteClassLevelCommand
from application.repository import ClassLevelRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteClassLevelUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        class_level_repository: ClassLevelRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__class_level_repository = class_level_repository

    async def execute(self, command: DeleteClassLevelCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__class_level_repository.id_exists(command.class_level_id):
            raise DomainError.not_found(
                f"уровень с id {command.class_level_id} не существует"
            )
        await self.__class_level_repository.delete(command.class_level_id)
