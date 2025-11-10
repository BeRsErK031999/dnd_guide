from abc import ABC, abstractmethod
from uuid import UUID

from domain.source import Source


class SourceRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, source_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, source_id: UUID) -> Source:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Source]:
        raise NotImplemented

    @abstractmethod
    async def save(self, source: Source) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, source_id: UUID) -> None:
        raise NotImplemented
