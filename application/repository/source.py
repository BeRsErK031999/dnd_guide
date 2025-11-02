from abc import ABC, abstractmethod
from uuid import UUID

from domain.source.source import Source


class SourceRepository(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_source_of_id_exist(self, source_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_source_of_id(self, source_id: UUID) -> Source:
        raise NotImplemented

    @abstractmethod
    async def save(self, source: Source) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, source_id: UUID) -> None:
        raise NotImplemented
