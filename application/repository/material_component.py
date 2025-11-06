from abc import ABC, abstractmethod
from uuid import UUID

from domain.material_component import MaterialComponent


class MaterialComponentRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_material_of_id_exist(self, material_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_material_of_id(self, material_id: UUID) -> MaterialComponent:
        raise NotImplemented

    @abstractmethod
    async def save(self, material: MaterialComponent) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, material_id: UUID) -> None:
        raise NotImplemented
