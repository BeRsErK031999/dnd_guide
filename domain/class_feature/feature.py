from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName, EntityNameInEnglish


class ClassFeature(EntityName, EntityNameInEnglish, EntityDescription):
    def __init__(
        self,
        feature_id: UUID,
        class_id: UUID,
        name: str,
        description: str,
        level: int,
        name_in_english: str,
    ) -> None:
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        EntityNameInEnglish.__init__(self, name_in_english)
        self._validate_level(level)
        self._feature_id = feature_id
        self._class_id = class_id
        self._level = level

    def feature_id(self) -> UUID:
        return self._feature_id

    def class_id(self) -> UUID:
        return self._class_id

    def level(self) -> int:
        return self._level

    def new_class_id(self, class_id: UUID) -> None:
        if self._class_id == class_id:
            raise DomainError.idempotent("текущий класс равен новому")
        self._class_id = class_id

    def new_level(self, level: int) -> None:
        if self._level == level:
            raise DomainError.idempotent(
                "текущее уровень умения равен новому уровень умения"
            )
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
