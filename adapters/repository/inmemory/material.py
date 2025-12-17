from uuid import UUID, uuid4

from application.dto.model.material import AppMaterial
from application.repository import MaterialRepository as AppMaterialRepository
from domain.material import MaterialRepository as DomainMaterialRepository


class InMemoryMaterialRepository(DomainMaterialRepository, AppMaterialRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppMaterial] = {}

    async def name_exists(self, name: str) -> bool:
        return any(material.name == name for material in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, material_id: UUID) -> bool:
        return material_id in self._store

    async def get_by_id(self, material_id: UUID) -> AppMaterial:
        return self._store[material_id]

    async def get_all(self) -> list[AppMaterial]:
        return list(self._store.values())

    async def filter(self, search_by_name: str | None = None) -> list[AppMaterial]:
        if search_by_name is not None:
            return [m for m in self._store.values() if search_by_name in m.name]
        return list(self._store.values())

    async def save(self, material: AppMaterial) -> None:
        self._store[material.material_id] = material

    async def delete(self, material_id: UUID) -> None:
        del self._store[material_id]
