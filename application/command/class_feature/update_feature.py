from uuid import UUID

from application.command.class_feature.base_command import BaseCommand
from domain.character_class_feature import (
    ClassFeatureDescription,
    ClassFeatureID,
    ClassFeatureLevel,
    ClassFeatureName,
)
from domain.error import DomainError
from domain.user import UserID


class UpdateClassFeatureCommand(BaseCommand):
    def execute(
        self,
        row_user_id: UUID,
        row_feature_id: UUID,
        row_name: str | None = None,
        row_level: int | None = None,
        row_description: str | None = None,
    ) -> None:
        self.assert_access(UserID(row_user_id))
        if all([row_name is None, row_level is None, row_description is None]):
            raise DomainError.invalid_data("не передано данных для обновления")
        feature_id = ClassFeatureID(row_feature_id)
        name = ClassFeatureName(row_name) if row_name is not None else None
        level = ClassFeatureLevel(row_level) if row_level is not None else None
        description = (
            ClassFeatureDescription(row_description)
            if row_description is not None
            else None
        )
        if not self.__feature_repository.is_class_feature_of_id_exist(feature_id):
            raise DomainError.not_found(f"умения с id {feature_id} не существует")
        feature = self.__feature_repository.get_class_feature_of_id(feature_id)
        if name is not None:
            feature.new_name(name)
        if level is not None:
            feature.new_level(level)
        if description is not None:
            feature.new_description(description)
        self.__feature_repository.class_feature_update(feature)
