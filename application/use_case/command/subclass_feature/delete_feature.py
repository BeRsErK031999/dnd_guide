from application.dto.command.subclass_feature import DeleteSubclassFeatureCommand
from application.repository import SubclassFeatureRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteSubclassFeatureUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        feature_repository: SubclassFeatureRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__feature_repository = feature_repository

    async def execute(self, command: DeleteSubclassFeatureCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__feature_repository.is_feature_of_id_exist(
            command.feature_id
        ):
            raise DomainError.not_found(
                f"умение подкласса с id {command.feature_id} не существует"
            )
        await self.__feature_repository.delete(command.feature_id)
