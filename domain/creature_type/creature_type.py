from uuid import UUID

from domain.creature_type.name import CreatureTypeName
from domain.error import DomainError


class CreatureType:
    def __init__(self, type_id: UUID, name: CreatureTypeName, description: str) -> None:
        self.__validate_description(description)
        self.__creature_type_id = type_id
        self.__name = name
        self.__description = description

    def creature_type_id(self) -> UUID:
        return self.__creature_type_id

    def name(self) -> CreatureTypeName:
        return self.__name

    def description(self) -> str:
        return self.__description

    def new_name(self, name: CreatureTypeName) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название типа существа равно новому названию типа существа"
            )
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data(
                "описание типа существа не может быть пустым"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__creature_type_id == value.__creature_type_id
        if isinstance(value, UUID):
            return self.__creature_type_id == value
        raise NotImplemented
