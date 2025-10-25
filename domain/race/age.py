from domain.error import DomainError


class RaceAge:
    def __init__(self, max_age: int, description: str) -> None:
        self.__validate_description(description)
        self.__max_age = max_age
        self.__description = description

    def max_age(self) -> int:
        return self.__max_age

    def description(self) -> str:
        return self.__description

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data(
                "описание возраста расы не может быть пустым"
            )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__max_age == value.__max_age
                and self.__description == value.__description
            )
        raise NotImplemented
