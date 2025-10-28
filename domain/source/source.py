from uuid import UUID

from domain.error import DomainError


class Source:
    def __init__(
        self,
        source_id: UUID,
        name: str,
        description: str,
        name_in_english: str,
    ) -> None:
        self.__validate_description(description)
        self.__validate_name(name)
        self.__validate_name_in_english(name_in_english)
        self.__source_id = source_id
        self.__name = name
        self.__name_in_english = name_in_english
        self.__description = description

    def source_id(self) -> UUID:
        return self.__source_id

    def name(self) -> str:
        return self.__name

    def name_in_english(self) -> str:
        return self.__name_in_english

    def description(self) -> str:
        return self.__description

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent("текущее название равно новому названию")
        self.__validate_name(name)
        self.__name = name

    def new_name_in_english(self, name_in_english: str) -> None:
        if self.__name_in_english == name_in_english:
            raise DomainError.idempotent(
                "текущее название на английском равно новому названию на английском"
            )
        self.__validate_name_in_english(name_in_english)
        self.__name_in_english = name_in_english

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название источника не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название источника не может превышать длину в 50 символов"
            )

    def __validate_name_in_english(self, name_in_english: str) -> None:
        if len(name_in_english) > 50:
            raise DomainError.invalid_data(
                "название источника на английском не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание источника не может быть пустым")

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__source_id == value.__source_id
        if isinstance(value, UUID):
            return self.__source_id == value
        raise NotImplemented
