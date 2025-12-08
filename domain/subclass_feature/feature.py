from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName, EntityNameInEnglish


class SubclassFeature(EntityName, EntityDescription, EntityNameInEnglish):
    def __init__(
        self,
        feature_id: UUID,
        subclass_id: UUID,
        name: str,
        description: str,
        level: int,
        name_in_english: str,
    ) -> None:
        self._validate_level(level)
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        EntityNameInEnglish.__init__(self, name_in_english)
        self._feature_id = feature_id
        self._subclass_id = subclass_id
        self._level = level

    def feature_id(self) -> UUID:
        return self._feature_id

    def subclass_id(self) -> UUID:
        return self._subclass_id

    def level(self) -> int:
        return self._level

    def new_subclass_id(self, subclass_id: UUID) -> None:
        if self._subclass_id == subclass_id:
            raise DomainError.idempotent("текущий подкласс равен новому")
        self._subclass_id = subclass_id

    def new_level(self, level: int) -> None:
        if self._level == level:
            raise DomainError.idempotent("текущее уровень умения равен новому")
        self._validate_level(level)
        self._level = level

    def _validate_level(self, level: int) -> None:
        if level < 1 or level > 20:
            raise DomainError.invalid_data(
                "уровень умения должен находиться в диапазоне от 1 до 20"
            )

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._feature_id == value._feature_id
        if isinstance(value, UUID):
            return self._feature_id == value
        raise NotImplemented
