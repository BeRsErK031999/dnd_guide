from typing import Sequence
from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName, EntityNameInEnglish
from domain.subrace.feature import SubraceFeature
from domain.subrace.increase_modifier import SubraceIncreaseModifier


class Subrace(EntityName, EntityDescription, EntityNameInEnglish):
    def __init__(
        self,
        subrace_id: UUID,
        race_id: UUID,
        name: str,
        description: str,
        increase_modifiers: Sequence[SubraceIncreaseModifier],
        features: Sequence[SubraceFeature],
        name_in_english: str,
    ) -> None:
        self.__validate_features(features)
        self.__validate_increase_modifiers(increase_modifiers)
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        EntityNameInEnglish.__init__(self, name_in_english)
        self.__subrace_id = subrace_id
        self.__race_id = race_id
        self.__increase_modifiers = list(increase_modifiers)
        self.__features = list(features)

    def subrace_id(self) -> UUID:
        return self.__subrace_id

    def race_id(self) -> UUID:
        return self.__race_id

    def increase_modifiers(self) -> list[SubraceIncreaseModifier]:
        return self.__increase_modifiers

    def features(self) -> list[SubraceFeature]:
        return self.__features

    def new_race_id(self, race_id: UUID) -> None:
        if self.__race_id == race_id:
            raise DomainError.idempotent("текущая раса ровна новой расе")
        self.__race_id = race_id

    def new_increase_modifiers(
        self, increase_modifiers: Sequence[SubraceIncreaseModifier]
    ) -> None:
        self.__validate_increase_modifiers(increase_modifiers)
        self.__increase_modifiers = list(increase_modifiers)

    def new_features(self, features: Sequence[SubraceFeature]) -> None:
        self.__validate_features(features)
        self.__features = list(features)

    def add_features(self, features: Sequence[SubraceFeature]) -> None:
        if len(features) == 0:
            raise DomainError.invalid_data(
                "список для добавления умений не может быть пустым"
            )
        self.__validate_features(features)
        for feature in features:
            if feature in self.__features:
                raise DomainError.invalid_data(
                    f"умение с названием {feature.name()} уже существует"
                )
        self.__features.extend(features)

    def remove_features(self, feature_names: Sequence[str]) -> None:
        if len(feature_names) == 0:
            raise DomainError.invalid_data(
                "список названий для удаления умений не может быть пустым"
            )
        removing_indexes = list()
        for i, feature in enumerate(self.__features):
            if feature.name() in feature_names:
                removing_indexes.append(i)
        [self.__features.pop(i) for i in removing_indexes]

    def __validate_features(self, features: Sequence[SubraceFeature]) -> None:
        if len(features) == 0:
            return
        temp = [feature.name() for feature in features]
        if len(temp) != len(set(temp)):
            raise DomainError.invalid_data("умения содержат дубликаты")

    def __validate_increase_modifiers(
        self, increase_modifiers: Sequence[SubraceIncreaseModifier]
    ) -> None:
        if len(increase_modifiers) == 0:
            return
        temp = [
            increase_modifier.modifier() for increase_modifier in increase_modifiers
        ]
        if len(temp) != len(set(temp)):
            raise DomainError.invalid_data(
                "увеличения модификаторов содержит дубликаты"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__subrace_id == value.__subrace_id
        if isinstance(value, UUID):
            return self.__subrace_id == value
        raise NotImplemented
