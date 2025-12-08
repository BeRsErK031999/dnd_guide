from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription


class Source(EntityDescription):
    def __init__(
        self,
        source_id: UUID,
        name: str,
        description: str,
        name_in_english: str,
    ) -> None:
        self._validate_name_in_english(name_in_english)
        self._validate_name(name)
        EntityDescription.__init__(self, description)
        self._source_id = source_id
        self._name = name
        self._name_in_english = name_in_english

    def source_id(self) -> UUID:
        return self._source_id

    def name(self) -> str:
        return self._name

    def name_in_english(self) -> str:
        return self._name_in_english

    def new_name(self, name: str) -> None:
        if self._name == name:
            raise DomainError.idempotent("текущее название равно новому названию")
        self._validate_name(name)
        self._name = name

    def new_name_in_english(self, name_in_english: str) -> None:
        if self._name_in_english == name_in_english:
            raise DomainError.idempotent(
                "текущее название на английском равно новому названию на английском"
            )
        self._validate_name_in_english(name_in_english)
        self._name_in_english = name_in_english

    def _validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название не может быть пустым")
        if len(name) > 100:
            raise DomainError.invalid_data(
                "название не может содержать более 100 символов"
            )

    def _validate_name_in_english(self, name_in_english: str) -> None:
        if len(name_in_english) > 100:
            raise DomainError.invalid_data(
                "название на английском не может содержать более 100 символов"
            )

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._source_id == value._source_id
        if isinstance(value, UUID):
            return self._source_id == value
        raise NotImplemented
