from uuid import UUID, uuid4

from application.dto.model.source import AppSource
from application.repository import SourceRepository as AppSourceRepository
from domain.source import SourceRepository as DomainSourceRepository


class InMemorySourceRepository(DomainSourceRepository, AppSourceRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppSource] = {}

    async def name_exists(self, name: str) -> bool:
        return any(source.name == name for source in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, source_id: UUID) -> bool:
        return source_id in self._store

    async def get_by_id(self, source_id: UUID) -> AppSource:
        return self._store[source_id]

    async def get_all(self) -> list[AppSource]:
        return list(self._store.values())

    async def filter(self, search_by_name: str | None = None) -> list[AppSource]:
        if search_by_name is not None:
            return [s for s in self._store.values() if search_by_name in s.name]
        return list(self._store.values())

    async def save(self, source: AppSource) -> None:
        self._store[source.source_id] = source

    async def delete(self, source_id: UUID) -> None:
        del self._store[source_id]
