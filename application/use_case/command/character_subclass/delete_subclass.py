from application.dto.command.character_subclass import DeleteSubclassCommand
from application.repository import SubclassRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteSubclassUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        subclass_repository: SubclassRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__subclass_repository = subclass_repository

    async def execute(self, command: DeleteSubclassCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__subclass_repository.id_exists(command.subclass_id):
            raise DomainError.not_found(
                f"подкласс с id {command.subclass_id} не существует"
            )
        await self.__subclass_repository.delete(command.subclass_id)
