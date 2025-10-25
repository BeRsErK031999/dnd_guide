from uuid import UUID

from domain.error import DomainError


class CharacterSubclass:
    def __init__(
        self, subclass_id: UUID, class_id: UUID, name: str, description: str
    ) -> None:
        self.__validate_name(name)
        self.__validate_description(description)
        self.__subclass_id = subclass_id
        self.__class_id = class_id
        self.__name = name
        self.__description = description

    def subclass_id(self) -> UUID:
        return self.__subclass_id

    def class_id(self) -> UUID:
        return self.__class_id

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def new_name(self, name) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название подкласса равно новому названию подкласса"
            )
        self.__validate_name(name)
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название подкласса не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название подкласса не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание подкласса не может быть пустым")

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__subclass_id == value.__subclass_id
        if isinstance(value, UUID):
            return self.__subclass_id == value
        raise NotImplemented
