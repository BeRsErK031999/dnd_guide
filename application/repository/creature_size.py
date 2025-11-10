from abc import ABC, abstractmethod
from uuid import UUID

from domain.creature_size import CreatureSize


class CreatureSizeRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, size_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, size_id: UUID) -> CreatureSize:
        raise NotImplemented

    @abstractmethod
    async def save(self, size: CreatureSize) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, size_id: UUID) -> None:
        raise NotImplemented
