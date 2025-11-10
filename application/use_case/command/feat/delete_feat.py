from application.dto.command.feat import DeleteFeatCommand
from application.repository import FeatRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteFeatUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        feat_repository: FeatRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__feat_repository = feat_repository

    async def execute(self, command: DeleteFeatCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__feat_repository.id_exists(command.feat_id):
            raise DomainError.not_found(f"черты с id {command.feat_id} не существует")
        await self.__feat_repository.delete(command.feat_id)
