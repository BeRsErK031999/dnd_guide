from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.material import AppMaterial


class MaterialRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, material_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, material_id: UUID) -> AppMaterial:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppMaterial]:
        raise NotImplemented

    @abstractmethod
    async def filter(self, search_by_name: str | None = None) -> list[AppMaterial]:
        raise NotImplemented

    @abstractmethod
    async def save(self, material: AppMaterial) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, material_id: UUID) -> None:
        raise NotImplemented
