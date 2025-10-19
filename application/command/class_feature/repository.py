from abc import ABC, abstractmethod

from domain.character_class.class_id import ClassID
from domain.character_class_feature.feature import ClassFeature
from domain.character_class_feature.feature_id import ClassFeatureID
from domain.character_class_feature.name import ClassFeatureName


class ClassFeatureRepository(ABC):
    @abstractmethod
    def next_id(self) -> ClassFeatureID:
        raise NotImplementedError()

    @abstractmethod
    def is_feature_of_id_exist(self, feature_id: ClassFeatureID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_feature_of_class_exist(
        self, class_id: ClassID, feature_id: ClassFeatureID
    ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_feature_name_of_class_exist(
        self, class_id: ClassID, feature_name: ClassFeatureName
    ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_feature_of_id(self, feature_id: ClassFeatureID) -> ClassFeature:
        raise NotImplementedError()

    @abstractmethod
    def feature_create(self, feature: ClassFeature) -> None:
        raise NotImplementedError()

    @abstractmethod
    def feature_update(self, feature: ClassFeature) -> None:
        raise NotImplementedError()
