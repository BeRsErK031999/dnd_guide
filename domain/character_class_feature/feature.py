from domain.character_class import ClassID
from domain.character_class_feature.description import ClassFeatureDescription
from domain.character_class_feature.feature_id import ClassFeatureID
from domain.character_class_feature.name import ClassFeatureName


class ClassFeature:
    def __init__(
        self,
        feature_id: ClassFeatureID,
        class_id: ClassID,
        name: ClassFeatureName,
        description: ClassFeatureDescription,
    ) -> None:
        self.__feature_id = feature_id
        self.__class_id = class_id
        self.__name = name
        self.__description = description

    def feature_id(self) -> ClassFeatureID:
        return self.__feature_id

    def class_id(self) -> ClassID:
        return self.__class_id

    def name(self) -> ClassFeatureName:
        return self.__name

    def description(self) -> ClassFeatureDescription:
        return self.__description

    def new_description(self, description: ClassFeatureDescription) -> None:
        self.__description = description

    def __str__(self) -> str:
        return f"название: {self.__name}"
