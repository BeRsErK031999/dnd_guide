from uuid import UUID, uuid4

from app_error import AppError
from application.repositories import ClassFeatureRepository
from domain.character_class import ClassID
from domain.character_class_feature import (
    ClassFeature,
    ClassFeatureID,
    ClassFeatureName,
)


class InMemoryClassFeatureRepository(ClassFeatureRepository):
    def __init__(self) -> None:
        self.__class_feature_store: dict[UUID, ClassFeature] = dict()

    def next_class_feature_id(self) -> ClassFeatureID:
        return ClassFeatureID(uuid4())

    def is_class_feature_of_id_exist(self, feature_id: ClassFeatureID) -> bool:
        return bool(self.__class_feature_store.get(feature_id.feature_id(), False))

    def is_class_feature_of_class_exist(
        self, class_id: ClassID, feature_id: ClassFeatureID
    ) -> bool:
        feature = self.__class_feature_store.get(feature_id.feature_id(), None)
        if feature is None:
            return False
        return feature.class_id() == class_id

    def is_class_feature_name_of_class_exist(
        self, class_id: ClassID, feature_name: ClassFeatureName
    ) -> bool:
        for _, feature in self.__class_feature_store.items():
            if feature.class_id() == class_id and feature.name() == feature_name:
                return True
        return False

    def get_class_feature_of_id(self, feature_id: ClassFeatureID) -> ClassFeature:
        feature = self.__class_feature_store.get(feature_id.feature_id(), None)
        if feature is None:
            raise AppError.internal(f"умения класса с id {feature_id} не существует")
        return feature

    def class_feature_create(self, feature: ClassFeature) -> None:
        if self.is_class_feature_of_id_exist(feature.feature_id()):
            raise AppError.internal(
                f"умения класса с id {feature.feature_id()} уже существует"
            )
        self.__class_feature_store[feature.feature_id().feature_id()] = feature

    def class_feature_update(self, feature: ClassFeature) -> None:
        if not self.is_class_feature_of_id_exist(feature.feature_id()):
            raise AppError.internal(
                f"умения класса с id {feature.feature_id()} не существует"
            )
        self.__class_feature_store[feature.feature_id().feature_id()] = feature
