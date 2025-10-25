from uuid import UUID

from domain.error import DomainError


class ClassFeature:
    def __init__(
        self,
        feature_id: UUID,
        class_id: UUID,
        name: str,
        description: str,
        level: int,
    ) -> None:
        self.__validate_description(description)
        self.__validate_name(name)
        self.__validate_level(level)
        self.__feature_id = feature_id
        self.__class_id = class_id
        self.__name = name
        self.__description = description
        self.__level = level

    def feature_id(self) -> UUID:
        return self.__feature_id

    def class_id(self) -> UUID:
        return self.__class_id

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def level(self) -> int:
        return self.__level

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название умения равно новому названию умения"
            )
        self.__validate_name(name)
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def new_level(self, level: int) -> None:
        if self.__level == level:
            raise DomainError.idempotent(
                "текущее уровень умения равен новому уровень умения"
            )
        self.__validate_level(level)
        self.__level = level

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название умения не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название умения не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание умения не может быть пустым")

    def __validate_level(self, level: int) -> None:
        if level < 1 or level > 20:
            raise DomainError.invalid_data(
                "уровень умения должен находиться в диапазоне от 1 до 20"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__feature_id == value.__feature_id
        if isinstance(value, UUID):
            return self.__feature_id == value
        raise NotImplemented
