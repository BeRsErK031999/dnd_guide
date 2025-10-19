from uuid import UUID

from application.command.class_feature.base_command import BaseCommand
from domain.character_class import ClassID
from domain.character_class_feature import (
    ClassFeature,
    ClassFeatureDescription,
    ClassFeatureLevel,
    ClassFeatureName,
)
from domain.error import DomainError
from domain.user import UserID


class NewClassFeatureCommand(BaseCommand):
    def execute(
        self,
        row_user_id: UUID,
        row_class_id: UUID,
        row_name: str,
        row_level: int,
        row_description: str,
    ) -> None:
        self.assert_access(UserID(row_user_id))
        class_id = ClassID(row_class_id)
        name = ClassFeatureName(row_name)
        level = ClassFeatureLevel(row_level)
        description = ClassFeatureDescription(row_description)
        if self.__feature_repository.is_class_feature_name_of_class_exist(
            class_id, name
        ):
            raise DomainError.idempotent(
                f"для класса уже существует умение с названием {name}"
            )
        feature = ClassFeature(
            self.__feature_repository.next_id(), class_id, name, level, description
        )
        self.__feature_repository.class_feature_create(feature)
