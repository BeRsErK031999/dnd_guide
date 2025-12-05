from uuid import UUID

from application.dto.command.class_feature import CreateClassFeatureCommand
from application.dto.model.class_feature import AppClassFeature
from application.repository import (
    ClassFeatureRepository,
    ClassRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.class_feature import ClassFeature, ClassFeatureService
from domain.error import DomainError


class CreateClassFeatureUseCase(UserCheck):
    def __init__(
        self,
        feature_service: ClassFeatureService,
        user_repository: UserRepository,
        class_repository: ClassRepository,
        feature_repository: ClassFeatureRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__feature_service = feature_service
        self.__class_repository = class_repository
        self.__feature_repository = feature_repository

    async def execute(self, command: CreateClassFeatureCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self.__feature_service.can_create_for_class_with_name(
            command.class_id, command.name
        ):
            raise DomainError.invalid_data(
                f"умение для класса с название {command.name} уже существует"
            )
        if not await self.__class_repository.id_exists(command.class_id):
            raise DomainError.invalid_data(
                f"класс с id {command.class_id} не существует"
            )
        feature = ClassFeature(
            await self.__feature_repository.next_id(),
            command.class_id,
            command.name,
            command.description,
            command.level,
            command.name_in_english,
        )
        await self.__feature_repository.create(AppClassFeature.from_domain(feature))
        return feature.feature_id()
