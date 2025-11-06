from uuid import UUID, uuid4

from application.repository import CreatureSizeRepository as AppCreatureSizeRepository
from domain.creature_size import CreatureSize
from domain.creature_size import CreatureSizeRepository as DomainCreatureSizeRepository


class InMemoryCreatureSizeRepository(
    DomainCreatureSizeRepository, AppCreatureSizeRepository
):
    def __init__(self) -> None:
        self.__store: dict[UUID, CreatureSize] = {}

    async def is_name_exist(self, name: str) -> bool:
        return any(size.name == name for size in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def is_size_of_id_exist(self, size_id: UUID) -> bool:
        return size_id in self.__store

    async def get_size_of_id(self, size_id: UUID) -> CreatureSize:
        return self.__store[size_id]

    async def save(self, size: CreatureSize) -> None:
        self.__store[size.size_id()] = size

    async def delete(self, size_id: UUID) -> None:
        del self.__store[size_id]
