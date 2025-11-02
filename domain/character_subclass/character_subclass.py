from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName


class CharacterSubclass(EntityName, EntityDescription):
    def __init__(
        self, subclass_id: UUID, class_id: UUID, name: str, description: str
    ) -> None:
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self.__subclass_id = subclass_id
        self.__class_id = class_id

    def subclass_id(self) -> UUID:
        return self.__subclass_id

    def class_id(self) -> UUID:
        return self.__class_id

    def new_class_id(self, class_id: UUID) -> None:
        if self.__class_id == class_id:
            raise DomainError.idempotent("текущий класс равен новому")
        self.__class_id = class_id

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__subclass_id == value.__subclass_id
        if isinstance(value, UUID):
            return self.__subclass_id == value
        raise NotImplemented
