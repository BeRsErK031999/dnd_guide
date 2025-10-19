from abc import ABC, abstractmethod

from domain.character_class import ClassID
from domain.character_class_feature import (
    ClassFeature,
    ClassFeatureID,
    ClassFeatureName,
)


class ClassFeatureRepository(ABC):
    @abstractmethod
    def next_class_feature_id(self) -> ClassFeatureID:
        raise NotImplementedError()

    @abstractmethod
    def is_class_feature_of_id_exist(self, feature_id: ClassFeatureID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_class_feature_of_class_exist(
        self, class_id: ClassID, feature_id: ClassFeatureID
    ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_class_feature_name_of_class_exist(
        self, class_id: ClassID, feature_name: ClassFeatureName
    ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_class_feature_of_id(self, feature_id: ClassFeatureID) -> ClassFeature:
        raise NotImplementedError()

    @abstractmethod
    def class_feature_create(self, feature: ClassFeature) -> None:
        raise NotImplementedError()

    @abstractmethod
    def class_feature_update(self, feature: ClassFeature) -> None:
        raise NotImplementedError()
