from application.dto.command.subclass_feature import UpdateSubclassFeatureCommand
from application.repository import (
    SubclassFeatureRepository,
    SubclassRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.subclass_feature import SubclassFeatureService


class UpdateSubclassFeatureUseCase(UserCheck):
    def __init__(
        self,
        feature_service: SubclassFeatureService,
        user_repository: UserRepository,
        subclass_repository: SubclassRepository,
        feature_repository: SubclassFeatureRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__feature_service = feature_service
        self.__subclass_repository = subclass_repository
        self.__feature_repository = feature_repository

    async def execute(self, command: UpdateSubclassFeatureCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__feature_repository.id_exists(command.feature_id):
            raise DomainError.not_found(
                f"умения подкласса с id {command.feature_id} не существует"
            )
        feature = await self.__feature_repository.get_by_id(command.feature_id)
        if command.name is not None and command.subclass_id is not None:
            if not await self.__feature_service.can_rename_for_class_with_name(
                command.subclass_id, command.name
            ):
                raise DomainError.invalid_data(
                    f"умение для подкласса с название {command.name} уже существует"
                )
            if not await self.__subclass_repository.id_exists(command.subclass_id):
                raise DomainError.invalid_data(
                    f"класс с id {command.subclass_id} не существует"
                )
            feature.new_name(command.name)
            feature.new_subclass_id(command.subclass_id)
        if command.name is not None:
            if not await self.__feature_service.can_rename_for_class_with_name(
                feature.subclass_id(), command.name
            ):
                raise DomainError.invalid_data(
                    f"умение для подкласса с название {command.name} уже существует"
                )
            feature.new_name(command.name)
        if command.subclass_id is not None:
            if not await self.__feature_service.can_rename_for_class_with_name(
                command.subclass_id, feature.name()
            ):
                raise DomainError.invalid_data(
                    f"умение для подкласса с название {feature.name()} уже существует"
                )
            if not await self.__subclass_repository.id_exists(command.subclass_id):
                raise DomainError.invalid_data(
                    f"подкласс с id {command.subclass_id} не существует"
                )
            feature.new_subclass_id(command.subclass_id)
        if command.description is not None:
            feature.new_description(command.description)
        if command.level is not None:
            feature.new_level(command.level)
        await self.__feature_repository.save(feature)
