from abc import ABC, abstractmethod
from uuid import UUID

from domain.material import Material


class MaterialRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, material_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, material_id: UUID) -> Material:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Material]:
        raise NotImplemented

    @abstractmethod
    async def save(self, material: Material) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, material_id: UUID) -> None:
        raise NotImplemented
