from re import L
from uuid import UUID

from domain.error import DomainError


class ValueName:
    def __init__(self, name: str) -> None:
        self._validate_name(name)
        self._name = name

    def name(self) -> str:
        return self._name

    def _validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название не может содержать более 50 символов"
            )


class EntityName(ValueName):
    def __init__(self, name: str) -> None:
        self._validate_name(name)
        self._name = name

    def name(self) -> str:
        return self._name

    def new_name(self, name: str) -> None:
        if self._name == name:
            raise DomainError.idempotent("текущее название равно новому названию")
        self._validate_name(name)
        self._name = name

    def _validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название не может содержать более 50 символов"
            )


class ValueNameInEnglish:
    def __init__(self, name_in_english: str) -> None:
        self._validate_name_in_english(name_in_english)
        self._name_in_english = name_in_english

    def name_in_english(self) -> str:
        return self._name_in_english

    def _validate_name_in_english(self, name_in_english: str) -> None:
        if len(name_in_english) > 50:
            raise DomainError.invalid_data(
                "название на английском не может содержать более 50 символов"
            )


class EntityNameInEnglish(ValueNameInEnglish):
    def __init__(self, name_in_english: str) -> None:
        self._validate_name_in_english(name_in_english)
        self._name_in_english = name_in_english

    def name_in_english(self) -> str:
        return self._name_in_english

    def new_name_in_english(self, name_in_english: str) -> None:
        if self._name_in_english == name_in_english:
            raise DomainError.idempotent(
                "текущее название на английском равно новому названию на английском"
            )
        self._validate_name_in_english(name_in_english)
        self._name_in_english = name_in_english

    def _validate_name_in_english(self, name_in_english: str) -> None:
        if len(name_in_english) > 50:
            raise DomainError.invalid_data(
                "название на английском не может содержать более 50 символов"
            )


class ValueDescription:
    def __init__(self, description: str) -> None:
        self._validate_description(description)
        self._description = description

    def description(self) -> str:
        return self._description

    def _validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание не может быть пустым")


class EntityDescription:
    def __init__(self, description: str) -> None:
        self._validate_description(description)
        self._description = description

    def description(self) -> str:
        return self._description

    def new_description(self, description: str) -> None:
        self._validate_description(description)
        self._description = description

    def _validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание не может быть пустым")


class EntitySource:
    def __init__(self, source_id: UUID) -> None:
        self._source_id = source_id

    def source_id(self) -> UUID:
        return self._source_id

    def new_source_id(self, source_id: UUID) -> None:
        if self._source_id == source_id:
            raise DomainError.idempotent("текущий источник равен новому")
        self._source_id = source_id
        self._source_id = source_id
