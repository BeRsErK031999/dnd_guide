from abc import ABC, abstractmethod
from uuid import UUID

from domain.material import Material


class MaterialRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, race_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, race_id: UUID) -> Material:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Material]:
        raise NotImplemented

    @abstractmethod
    async def save(self, race: Material) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, race_id: UUID) -> None:
        raise NotImplemented
