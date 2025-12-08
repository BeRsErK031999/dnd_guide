from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName, EntityNameInEnglish


class CharacterSubclass(EntityName, EntityDescription, EntityNameInEnglish):
    def __init__(
        self,
        subclass_id: UUID,
        class_id: UUID,
        name: str,
        description: str,
        name_in_english: str,
    ) -> None:
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        EntityNameInEnglish.__init__(self, name_in_english)
        self._subclass_id = subclass_id
        self._class_id = class_id

    def subclass_id(self) -> UUID:
        return self._subclass_id

    def class_id(self) -> UUID:
        return self._class_id

    def new_class_id(self, class_id: UUID) -> None:
        if self._class_id == class_id:
            raise DomainError.idempotent("текущий класс равен новому")
        self._class_id = class_id

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._subclass_id == value._subclass_id
        if isinstance(value, UUID):
            return self._subclass_id == value
        raise NotImplemented
