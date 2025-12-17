from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.source import AppSource


class SourceRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, source_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, source_id: UUID) -> AppSource:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppSource]:
        raise NotImplemented

    @abstractmethod
    async def filter(self, search_by_name: str | None = None) -> list[AppSource]:
        raise NotImplemented

    @abstractmethod
    async def save(self, source: AppSource) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, source_id: UUID) -> None:
        raise NotImplemented
