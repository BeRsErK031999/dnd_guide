from typing import Sequence
from uuid import UUID

from domain.error import DomainError
from domain.race.age import RaceAge
from domain.race.feature import RaceFeature
from domain.race.increase_modifier import RaceIncreaseModifier
from domain.race.speed import RaceSpeed


class Race:
    def __init__(
        self,
        race_id: UUID,
        name: str,
        description: str,
        type_id: UUID,
        size_id: UUID,
        speed: RaceSpeed,
        age: RaceAge,
        increase_modifier: RaceIncreaseModifier,
        features: Sequence[RaceFeature],
    ) -> None:
        self.__validate_name(name)
        self.__validate_description(description)
        self.__validate_features(features)
        self.__race_id = race_id
        self.__name = name
        self.__description = description
        self.__type_id = type_id
        self.__size_id = size_id
        self.__speed = speed
        self.__age = age
        self.__increase_modifier = increase_modifier
        self.__features = list(features)

    def race_id(self) -> UUID:
        return self.__race_id

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def type_id(self) -> UUID:
        return self.__type_id

    def size_id(self) -> UUID:
        return self.__size_id

    def speed(self) -> RaceSpeed:
        return self.__speed

    def age(self) -> RaceAge:
        return self.__age

    def increase_modifier(self) -> RaceIncreaseModifier:
        return self.__increase_modifier

    def features(self) -> list[RaceFeature]:
        return self.__features

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название расы равно новому названию расы"
            )
        self.__validate_name(name)
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def new_type_id(self, type_id: UUID) -> None:
        if self.__type_id == type_id:
            raise DomainError.idempotent("текущий тип расы равен новому типу расы")
        self.__type_id = type_id

    def new_size_id(self, size_id: UUID) -> None:
        if self.__size_id == size_id:
            raise DomainError.idempotent(
                "текущий размер расы равен новому размеру расы"
            )
        self.__size_id = size_id

    def new_speed(self, speed: RaceSpeed) -> None:
        if self.__speed == speed:
            raise DomainError.idempotent(
                "текущий скорость расы равен новому скорости расы"
            )
        self.__speed = speed

    def new_age(self, age: RaceAge) -> None:
        if self.__age == age:
            raise DomainError.idempotent(
                "текущий возраст расы равен новому возрасту расы"
            )
        self.__age = age

    def new_increase_modifier(self, increase_modifier: RaceIncreaseModifier) -> None:
        if self.__increase_modifier == increase_modifier:
            raise DomainError.idempotent(
                "текущее увеличение характеристик расы равно новому увеличению характеристик расы"
            )
        self.__increase_modifier = increase_modifier

    def new_features(self, features: Sequence[RaceFeature]) -> None:
        self.__validate_features(features)
        self.__features = list(features)

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название расы не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название расы не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание расы не может быть пустым")

    def __validate_features(self, features: Sequence[RaceFeature]) -> None:
        if len(features) == 0:
            return
        temp = [feature.name() for feature in features]
        if len(temp) != len(set(temp)):
            raise DomainError.invalid_data("умения расы содержат дубликаты")

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__race_id == value.__race_id
        if isinstance(value, UUID):
            return self.__race_id == value
        raise NotImplemented
