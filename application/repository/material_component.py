from abc import ABC, abstractmethod
from uuid import UUID

from domain.material_component import MaterialComponent


class MaterialComponentRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, material_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, material_id: UUID) -> MaterialComponent:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[MaterialComponent]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self, search_by_name: str | None = None
    ) -> list[MaterialComponent]:
        raise NotImplemented

    @abstractmethod
    async def create(self, material: MaterialComponent) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, material: MaterialComponent) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, material_id: UUID) -> None:
        raise NotImplemented
