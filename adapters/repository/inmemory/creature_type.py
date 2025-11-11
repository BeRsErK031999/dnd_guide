from uuid import UUID, uuid4

from application.repository import CreatureTypeRepository as AppCreatureTypeRepository
from domain.creature_type import CreatureType
from domain.creature_type import CreatureTypeRepository as DomainCreatureTypeRepository


class InMemoryCreatureTypeRepository(
    DomainCreatureTypeRepository, AppCreatureTypeRepository
):
    def __init__(self) -> None:
        self.__store: dict[UUID, CreatureType] = {}

    async def name_exists(self, name: str) -> bool:
        return any(ct.name() == name for ct in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, creature_type_id: UUID) -> bool:
        return creature_type_id in self.__store

    async def get_by_id(self, creature_type_id: UUID) -> CreatureType:
        return self.__store[creature_type_id]

    async def get_all(self) -> list[CreatureType]:
        return list(self.__store.values())

    async def create(self, creature_type: CreatureType) -> None:
        self.__store[creature_type.creature_type_id()] = creature_type

    async def update(self, creature_type: CreatureType) -> None:
        self.__store[creature_type.creature_type_id()] = creature_type

    async def delete(self, creature_type_id: UUID) -> None:
        del self.__store[creature_type_id]
