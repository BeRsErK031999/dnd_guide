from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.material_component import AppMaterialComponent


class MaterialComponentRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, material_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, material_id: UUID) -> AppMaterialComponent:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppMaterialComponent]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self, search_by_name: str | None = None
    ) -> list[AppMaterialComponent]:
        raise NotImplemented

    @abstractmethod
    async def create(self, material: AppMaterialComponent) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, material: AppMaterialComponent) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, material_id: UUID) -> None:
        raise NotImplemented
