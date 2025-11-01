from uuid import UUID

from domain.mixin import EntityDescription, EntityName


class CreatureType(EntityName, EntityDescription):
    def __init__(self, type_id: UUID, name: str, description: str) -> None:
        EntityDescription.__init__(self, description)
        EntityName.__init__(self, name)
        self.__creature_type_id = type_id

    def creature_type_id(self) -> UUID:
        return self.__creature_type_id

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__creature_type_id == value.__creature_type_id
        if isinstance(value, UUID):
            return self.__creature_type_id == value
        raise NotImplemented
