from re import L

from domain.error import DomainError


class ValueName:
    def __init__(self, name: str) -> None:
        self.__validate_name(name)
        self.__name = name

    def name(self) -> str:
        return self.__name

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название не может содержать более 50 символов"
            )


class EntityName(ValueName):
    def __init__(self, name: str) -> None:
        self.__validate_name(name)
        self.__name = name

    def name(self) -> str:
        return self.__name

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent("текущее название равно новому названию")
        self.__validate_name(name)
        self.__name = name

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название не может содержать более 50 символов"
            )


class ValueNameInEnglish:
    def __init__(self, name_in_english: str) -> None:
        self.__validate_name_in_english(name_in_english)
        self.__name_in_english = name_in_english

    def name_in_english(self) -> str:
        return self.__name_in_english

    def __validate_name_in_english(self, name_in_english: str) -> None:
        if len(name_in_english) > 50:
            raise DomainError.invalid_data(
                "название на английском не может содержать более 50 символов"
            )


class EntityNameInEnglish(ValueNameInEnglish):
    def __init__(self, name_in_english: str) -> None:
        self.__validate_name_in_english(name_in_english)
        self.__name_in_english = name_in_english

    def name_in_english(self) -> str:
        return self.__name_in_english

    def new_name_in_english(self, name_in_english: str) -> None:
        if self.__name_in_english == name_in_english:
            raise DomainError.idempotent(
                "текущее название на английском равно новому названию на английском"
            )
        self.__validate_name_in_english(name_in_english)
        self.__name_in_english = name_in_english

    def __validate_name_in_english(self, name_in_english: str) -> None:
        if len(name_in_english) > 50:
            raise DomainError.invalid_data(
                "название на английском не может содержать более 50 символов"
            )


class ValueDescription:
    def __init__(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def description(self) -> str:
        return self.__description

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание не может быть пустым")


class EntityDescription:
    def __init__(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def description(self) -> str:
        return self.__description

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание не может быть пустым")
