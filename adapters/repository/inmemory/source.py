from uuid import UUID, uuid4

from application.repository import SourceRepository as AppSourceRepository
from domain.source import Source
from domain.source import SourceRepository as DomainSourceRepository


class InMemorySourceRepository(DomainSourceRepository, AppSourceRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, Source] = {}

    async def name_exists(self, name: str) -> bool:
        return any(source.name == name for source in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, source_id: UUID) -> bool:
        return source_id in self.__store

    async def get_by_id(self, source_id: UUID) -> Source:
        return self.__store[source_id]

    async def save(self, source: Source) -> None:
        self.__store[source.source_id()] = source

    async def delete(self, source_id: UUID) -> None:
        del self.__store[source_id]
