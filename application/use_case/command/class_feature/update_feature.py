from application.dto.command.class_feature import UpdateClassFeatureCommand
from application.repository import (
    ClassFeatureRepository,
    ClassRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.class_feature import ClassFeatureService
from domain.error import DomainError


class UpdateClassFeatureUseCase(UserCheck):
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

    async def execute(self, command: UpdateClassFeatureCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__feature_repository.id_exists(command.feature_id):
            raise DomainError.not_found(
                f"умения класса с id {command.feature_id} не существует"
            )
        feature = await self.__feature_repository.get_by_id(command.feature_id)
        if command.name is not None and command.class_id is not None:
            if not await self.__feature_service.can_rename_for_class_with_name(
                command.class_id, command.name
            ):
                raise DomainError.invalid_data(
                    f"умение для класса с название {command.name} уже существует"
                )
            if not await self.__class_repository.id_exists(command.class_id):
                raise DomainError.invalid_data(
                    f"класс с id {command.class_id} не существует"
                )
            feature.new_name(command.name)
            feature.new_class_id(command.class_id)
        if command.name is not None:
            if not await self.__feature_service.can_rename_for_class_with_name(
                feature.class_id(), command.name
            ):
                raise DomainError.invalid_data(
                    f"умение для класса с название {command.name} уже существует"
                )
            feature.new_name(command.name)
        if command.class_id is not None:
            if not await self.__feature_service.can_rename_for_class_with_name(
                command.class_id, feature.name()
            ):
                raise DomainError.invalid_data(
                    f"умение для класса с название {feature.name()} уже существует"
                )
            if not await self.__class_repository.id_exists(command.class_id):
                raise DomainError.invalid_data(
                    f"класс с id {command.class_id} не существует"
                )
            feature.new_class_id(command.class_id)
        if command.description is not None:
            feature.new_description(command.description)
        if command.level is not None:
            feature.new_level(command.level)
        await self.__feature_repository.save(feature)
