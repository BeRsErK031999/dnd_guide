from domain.error import DomainError
from domain.length import Length


class RaceSpeed:
    def __init__(self, base_speed: Length, description: str) -> None:
        self.__validate_description(description)
        self.__base_speed = base_speed
        self.__description = description

    def base_speed(self) -> Length:
        return self.__base_speed

    def description(self) -> str:
        return self.__description

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data(
                "описание скорости расы не может быть пустым"
            )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__base_speed == value.__base_speed
                and self.__description == value.__description
            )
        raise NotImplemented
