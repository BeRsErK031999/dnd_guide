from application.dto.command.subrace import DeleteSubraceCommand
from application.repository import SubraceRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteSubraceUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        subrace_repository: SubraceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__subrace_repository = subrace_repository

    async def execute(self, command: DeleteSubraceCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__subrace_repository.is_subrace_of_id_exist(
            command.subrace_id
        ):
            raise DomainError.not_found(
                f"подрасы с id {command.subrace_id} не существует"
            )
        await self.__subrace_repository.delete(command.subrace_id)
