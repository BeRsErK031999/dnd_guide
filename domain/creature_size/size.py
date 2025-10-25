from uuid import UUID

from domain.creature_size.size_name import CreatureSizeName
from domain.error import DomainError


class CreatureSize:
    def __init__(self, size_id: UUID, name: CreatureSizeName, description: str) -> None:
        self.__validate_description(description)
        self.__creature_size_id = size_id
        self.__name = name
        self.__description = description

    def creature_size_id(self) -> UUID:
        return self.__creature_size_id

    def name(self) -> CreatureSizeName:
        return self.__name

    def description(self) -> str:
        return self.__description

    def new_name(self, name: CreatureSizeName) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название размера существа равно новому названию размера существа"
            )
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data(
                "описание размера существа не может быть пустым"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__creature_size_id == value.__creature_size_id
        if isinstance(value, UUID):
            return self.__creature_size_id == value
        raise NotImplemented
