from uuid import UUID

from application.dto.command.subclass_feature import CreateSubclassFeatureCommand
from application.dto.model.subclass_feature import AppSubclassFeature
from application.repository import (
    SubclassFeatureRepository,
    SubclassRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.subclass_feature import SubclassFeature, SubclassFeatureService


class CreateSubclassFeatureUseCase(UserCheck):
    def __init__(
        self,
        feature_service: SubclassFeatureService,
        user_repository: UserRepository,
        subclass_repository: SubclassRepository,
        feature_repository: SubclassFeatureRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._feature_service = feature_service
        self._subclass_repository = subclass_repository
        self._feature_repository = feature_repository

    async def execute(self, command: CreateSubclassFeatureCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self._feature_service.can_create_for_subclass_with_name(
            command.subclass_id, command.name
        ):
            raise DomainError.invalid_data(
                f"умение для подкласса с название {command.name} уже существует"
            )
        if not await self._subclass_repository.id_exists(command.subclass_id):
            raise DomainError.invalid_data(
                f"подкласс с id {command.subclass_id} не существует"
            )
        feature = SubclassFeature(
            await self._feature_repository.next_id(),
            command.subclass_id,
            command.name,
            command.description,
            command.level,
            command.name_in_english,
        )
        await self._feature_repository.create(AppSubclassFeature.from_domain(feature))
        return feature.feature_id()
