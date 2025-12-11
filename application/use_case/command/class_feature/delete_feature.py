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
        self._feature_repository = feature_repository

    async def execute(self, command: DeleteClassFeatureCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._feature_repository.id_exists(command.feature_id):
            raise DomainError.not_found(
                f"умение класса с id {command.feature_id} не существует"
            )
        await self._feature_repository.delete(command.feature_id)
