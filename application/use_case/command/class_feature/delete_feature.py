from application.dto.command.class_feature import DeleteClassFeatureCommand
from application.repository import ClassFeatureRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteClassFeatureUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        feature_repository: ClassFeatureRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__feature_repository = feature_repository

    async def execute(self, command: DeleteClassFeatureCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__feature_repository.id_exists(command.feature_id):
            raise DomainError.not_found(
                f"умение класса с id {command.feature_id} не существует"
            )
        await self.__feature_repository.delete(command.feature_id)
