from domain.error import DomainError


class SubraceFeature:
    def __init__(
        self,
        name: str,
        description: str,
    ) -> None:
        self.__validate_name(name)
        self.__validate_description(description)
        self.__name = name
        self.__description = description

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data(
                "название умения подрасы не может быть пустым"
            )
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название умения подрасы не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data(
                "описание умения подрасы не может быть пустым"
            )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__name == value.__name
                and self.__description == value.__description
            )
        raise NotImplemented
