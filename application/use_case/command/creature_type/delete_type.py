from application.dto.command.creature_type import DeleteCreatureTypeCommand
from application.repository import CreatureTypeRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteCreatureTypeUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        creature_type_repository: CreatureTypeRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__type_repository = creature_type_repository

    async def execute(self, command: DeleteCreatureTypeCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__type_repository.is_type_of_id_exist(command.type_id):
            raise DomainError.not_found(
                f"типа существа с id {command.type_id} не существует"
            )
        await self.__type_repository.delete(command.type_id)
