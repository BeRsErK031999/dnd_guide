from typing import Sequence
from uuid import UUID

from domain.creature_size import CreatureSize
from domain.creature_type import CreatureType
from domain.error import DomainError
from domain.mixin import (
    EntityDescription,
    EntityName,
    EntityNameInEnglish,
    EntitySource,
)
from domain.race.age import RaceAge
from domain.race.feature import RaceFeature
from domain.race.increase_modifier import RaceIncreaseModifier
from domain.race.speed import RaceSpeed


class Race(EntityName, EntityDescription, EntityNameInEnglish, EntitySource):
    def __init__(
        self,
        race_id: UUID,
        name: str,
        description: str,
        creature_type: CreatureType,
        creature_size: CreatureSize,
        speed: RaceSpeed,
        age: RaceAge,
        increase_modifiers: Sequence[RaceIncreaseModifier],
        features: Sequence[RaceFeature],
        name_in_english: str,
        source_id: UUID,
    ) -> None:
        self._validate_features(features)
        self._validate_increase_modifiers(increase_modifiers)
        EntityName.__init__(self, name)
        EntityNameInEnglish.__init__(self, name_in_english)
        EntityDescription.__init__(self, description)
        EntitySource.__init__(self, source_id)
        self._race_id = race_id
        self._creature_type = creature_type
        self._creature_size = creature_size
        self._speed = speed
        self._age = age
        self._increase_modifiers = list(increase_modifiers)
        self._features = list(features)

    def race_id(self) -> UUID:
        return self._race_id

    def creature_type(self) -> CreatureType:
        return self._creature_type

    def creature_size(self) -> CreatureSize:
        return self._creature_size

    def speed(self) -> RaceSpeed:
        return self._speed

    def age(self) -> RaceAge:
        return self._age

    def increase_modifiers(self) -> list[RaceIncreaseModifier]:
        return self._increase_modifiers

    def features(self) -> list[RaceFeature]:
        return self._features

    def new_creature_type(self, creature_type: CreatureType) -> None:
        if self._creature_type == creature_type:
            raise DomainError.idempotent("текущий тип расы равен новому типу расы")
        self._creature_type = creature_type

    def new_creature_size(self, creature_size: CreatureSize) -> None:
        if self._creature_size == creature_size:
            raise DomainError.idempotent(
                "текущий размер расы равен новому размеру расы"
            )
        self._creature_size = creature_size

    def new_speed(self, speed: RaceSpeed) -> None:
        if self._speed == speed:
            raise DomainError.idempotent(
                "текущий скорость расы равен новому скорости расы"
            )
        self._speed = speed

    def new_age(self, age: RaceAge) -> None:
        if self._age == age:
            raise DomainError.idempotent(
                "текущий возраст расы равен новому возрасту расы"
            )
        self._age = age

    def new_increase_modifiers(
        self, increase_modifiers: Sequence[RaceIncreaseModifier]
    ) -> None:
        self._validate_increase_modifiers(increase_modifiers)
        self._increase_modifiers = list(increase_modifiers)

    def new_features(self, features: Sequence[RaceFeature]) -> None:
        self._validate_features(features)
        self._features = list(features)

    def add_features(self, features: Sequence[RaceFeature]) -> None:
        if len(features) == 0:
            raise DomainError.invalid_data(
                "список для добавления умений не может быть пустым"
            )
        self._validate_features(features)
        for feature in features:
            if feature in self._features:
                raise DomainError.invalid_data(
                    f"умение с названием {feature.name()} уже существует"
                )
        self._features.extend(features)

    def remove_features(self, feature_names: Sequence[str]) -> None:
        if len(feature_names) == 0:
            raise DomainError.invalid_data(
                "список названий для удаления умений не может быть пустым"
            )
        removing_indexes = list()
        for i, feature in enumerate(self._features):
            if feature.name() in feature_names:
                removing_indexes.append(i)
        [self._features.pop(i) for i in removing_indexes]

    def _validate_increase_modifiers(
        self, increase_modifiers: Sequence[RaceIncreaseModifier]
    ) -> None:
        if len(increase_modifiers) == 0:
            return
        temp = [
            increase_modifier.modifier() for increase_modifier in increase_modifiers
        ]
        if len(temp) != len(set(temp)):
            raise DomainError.invalid_data(
                "увеличения модификаторов расы содержат дубликаты"
            )

    def _validate_features(self, features: Sequence[RaceFeature]) -> None:
        if len(features) == 0:
            return
        temp = [feature.name() for feature in features]
        if len(temp) != len(set(temp)):
            raise DomainError.invalid_data("умения расы содержат дубликаты")

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._race_id == value._race_id
        if isinstance(value, UUID):
            return self._race_id == value
        raise NotImplemented
