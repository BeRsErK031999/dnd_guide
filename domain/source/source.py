from uuid import UUID

from domain.error import DomainError


class Source:
    def __init__(
        self,
        source_id: UUID,
        name: str,
        original_name: str,
        description: str,
    ) -> None:
        self.__validate_description(description)
        self.__validate_name(name)
        self.__validate_original_name(original_name)
        self.__source_id = source_id
        self.__name = name
        self.__original_name = original_name
        self.__description = description

    def source_id(self) -> UUID:
        return self.__source_id

    def name(self) -> str:
        return self.__name

    def original_name(self) -> str:
        return self.__original_name

    def description(self) -> str:
        return self.__description

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent("текущее название равно новому названию")
        self.__validate_name(name)
        self.__name = name

    def new_original_name(self, original_name: str) -> None:
        if self.__original_name == original_name:
            raise DomainError.idempotent(
                "текущее оригинальное название равно новому оригинальному названию"
            )
        self.__validate_original_name(original_name)
        self.__original_name = original_name

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

    def __validate_original_name(self, original_name: str) -> None:
        if len(original_name) == 0:
            raise DomainError.invalid_data(
                "оригинальное название источника не может быть пустым"
            )
        if len(original_name) > 50:
            raise DomainError.invalid_data(
                "оригинальное название источника не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание источника не может быть пустым")
