from uuid import UUID

from domain.creature_type.name import CreatureTypeName
from domain.error import DomainError
from domain.mixin import EntityDescription


class CreatureType(EntityDescription):
    def __init__(self, type_id: UUID, name: CreatureTypeName, description: str) -> None:
        EntityDescription.__init__(self, description)
        self.__creature_type_id = type_id
        self.__name = name

    def creature_type_id(self) -> UUID:
        return self.__creature_type_id

    def name(self) -> CreatureTypeName:
        return self.__name

    def new_name(self, name: CreatureTypeName) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название типа существа равно новому названию типа существа"
            )
        self.__name = name

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__creature_type_id == value.__creature_type_id
        if isinstance(value, UUID):
            return self.__creature_type_id == value
        raise NotImplemented
