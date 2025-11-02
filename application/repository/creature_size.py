from abc import ABC, abstractmethod
from uuid import UUID

from domain.creature_size.size import CreatureSize


class CreatureSizeRepository(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_size_of_id_exist(self, size_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_size_of_id(self, size_id: UUID) -> CreatureSize:
        raise NotImplemented

    @abstractmethod
    async def save(self, size: CreatureSize) -> None:
        raise NotImplemented
