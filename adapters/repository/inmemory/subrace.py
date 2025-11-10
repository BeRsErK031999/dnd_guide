from uuid import UUID, uuid4

from application.repository import SubraceRepository as AppSubraceRepository
from domain.subrace import Subrace
from domain.subrace import SubraceRepository as DomainSubraceRepository


class InMemorySubraceRepository(DomainSubraceRepository, AppSubraceRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, Subrace] = {}

    async def name_exists(self, name: str) -> bool:
        return any(subrace.name == name for subrace in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, subrace_id: UUID) -> bool:
        return subrace_id in self.__store

    async def get_by_id(self, subrace_id: UUID) -> Subrace:
        return self.__store[subrace_id]

    async def save(self, subrace: Subrace) -> None:
        self.__store[subrace.subrace_id()] = subrace

    async def delete(self, subrace_id: UUID) -> None:
        del self.__store[subrace_id]
