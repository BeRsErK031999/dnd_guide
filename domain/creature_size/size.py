from uuid import UUID

from domain.mixin import EntityDescription, EntityName


class CreatureSize(EntityName, EntityDescription):
    def __init__(self, size_id: UUID, name: str, description: str) -> None:
        EntityDescription.__init__(self, description)
        EntityName.__init__(self, name)
        self.__creature_size_id = size_id

    def size_id(self) -> UUID:
        return self.__creature_size_id

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__creature_size_id == value.__creature_size_id
        if isinstance(value, UUID):
            return self.__creature_size_id == value
        raise NotImplemented
