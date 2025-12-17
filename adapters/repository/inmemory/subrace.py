from uuid import UUID, uuid4

from application.dto.model.subrace import AppSubrace
from application.repository import SubraceRepository as AppSubraceRepository
from domain.subrace import SubraceRepository as DomainSubraceRepository


class InMemorySubraceRepository(DomainSubraceRepository, AppSubraceRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppSubrace] = {}

    async def name_exists(self, name: str) -> bool:
        return any(subrace.name == name for subrace in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, subrace_id: UUID) -> bool:
        return subrace_id in self._store

    async def get_by_id(self, subrace_id: UUID) -> AppSubrace:
        return self._store[subrace_id]

    async def get_all(self) -> list[AppSubrace]:
        return list(self._store.values())

    async def filter(self, search_by_name: str | None = None) -> list[AppSubrace]:
        if search_by_name is not None:
            return [s for s in self._store.values() if search_by_name in s.name]
        return list(self._store.values())

    async def save(self, subrace: AppSubrace) -> None:
        self._store[subrace.subrace_id] = subrace

    async def delete(self, subrace_id: UUID) -> None:
        del self._store[subrace_id]
