from typing import Sequence
from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName
from domain.subrace.feature import SubraceFeature
from domain.subrace.increase_modifier import SubraceIncreaseModifier


class Subrace(EntityName, EntityDescription):
    def __init__(
        self,
        subrace_id: UUID,
        race_id: UUID,
        name: str,
        description: str,
        increase_modifier: SubraceIncreaseModifier,
        features: Sequence[SubraceFeature],
    ) -> None:
        self.__validate_features(features)
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self.__subrace_id = subrace_id
        self.__race_id = race_id
        self.__increase_modifier = increase_modifier
        self.__features = list(features)

    def subrace_id(self) -> UUID:
        return self.__subrace_id

    def race_id(self) -> UUID:
        return self.__race_id

    def increase_modifier(self) -> SubraceIncreaseModifier:
        return self.__increase_modifier

    def features(self) -> list[SubraceFeature]:
        return self.__features

    def new_race_id(self, race_id: UUID) -> None:
        if self.__race_id == race_id:
            raise DomainError.idempotent("текущая раса ровна новой расе")
        self.__race_id = race_id

    def new_increase_modifier(self, increase_modifier: SubraceIncreaseModifier) -> None:
        if self.__increase_modifier == increase_modifier:
            raise DomainError.idempotent(
                "текущее увеличение характеристик подрасы равно новому увеличению характеристик подрасы"
            )
        self.__increase_modifier = increase_modifier

    def new_features(self, features: Sequence[SubraceFeature]) -> None:
        self.__validate_features(features)
        self.__features = list(features)

    def __validate_features(self, features: Sequence[SubraceFeature]) -> None:
        if len(features) == 0:
            return
        temp = [feature.name() for feature in features]
        if len(temp) != len(set(temp)):
            raise DomainError.invalid_data("умения подрасы содержат дубликаты")

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__subrace_id == value.__subrace_id
        if isinstance(value, UUID):
            return self.__subrace_id == value
        raise NotImplemented
