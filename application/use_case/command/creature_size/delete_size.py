from application.dto.command.creature_size import DeleteCreatureSizeCommand
from application.repository import CreatureSizeRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteCreatureSizeUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        creature_size_repository: CreatureSizeRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__size_repository = creature_size_repository

    async def execute(self, command: DeleteCreatureSizeCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__size_repository.is_size_of_id_exist(command.size_id):
            raise DomainError.not_found(
                f"размера существ с id {command.size_id} не существует"
            )
        await self.__size_repository.delete(command.size_id)
