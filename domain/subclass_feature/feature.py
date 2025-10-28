from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName


class SubclassFeature(EntityName, EntityDescription):
    def __init__(
        self,
        feature_id: UUID,
        subclass_id: UUID,
        name: str,
        description: str,
        level: int,
    ) -> None:
        self.__validate_level(level)
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self.__feature_id = feature_id
        self.__subclass_id = subclass_id
        self.__level = level

    def feature_id(self) -> UUID:
        return self.__feature_id

    def subclass_id(self) -> UUID:
        return self.__subclass_id

    def level(self) -> int:
        return self.__level

    def new_level(self, level: int) -> None:
        if self.__level == level:
            raise DomainError.idempotent(
                "текущее уровень умения равен новому уровень умения"
            )
        self.__validate_level(level)
        self.__level = level

    def __validate_level(self, level: int) -> None:
        if level < 1 or level > 20:
            raise DomainError.invalid_data(
                "уровень умения должен находиться в диапазоне от 1 до 20"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__feature_id == value.__feature_id
        if isinstance(value, UUID):
            return self.__feature_id == value
        raise NotImplemented
