from uuid import UUID, uuid4

from application.repository import MaterialRepository as AppMaterialRepository
from domain.material import Material
from domain.material import MaterialRepository as DomainMaterialRepository


class InMemoryMaterialRepository(DomainMaterialRepository, AppMaterialRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, Material] = {}

    async def name_exists(self, name: str) -> bool:
        return any(material.name() == name for material in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, material_id: UUID) -> bool:
        return material_id in self.__store

    async def get_by_id(self, material_id: UUID) -> Material:
        return self.__store[material_id]

    async def get_all(self) -> list[Material]:
        return list(self.__store.values())

    async def create(self, material: Material) -> None:
        self.__store[material.material_id()] = material

    async def update(self, material: Material) -> None:
        self.__store[material.material_id()] = material

    async def delete(self, material_id: UUID) -> None:
        del self.__store[material_id]
