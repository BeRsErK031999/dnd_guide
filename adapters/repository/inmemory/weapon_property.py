from uuid import UUID, uuid4

from application.dto.model.weapon_property import AppWeaponProperty
from application.repository import (
    WeaponPropertyRepository as AppWeaponPropertyRepository,
)
from domain.weapon_property import (
    WeaponPropertyRepository as DomainWeaponPropertyRepository,
)


class InMemoryWeaponPropertyRepository(
    DomainWeaponPropertyRepository, AppWeaponPropertyRepository
):
    def __init__(self) -> None:
        self._store: dict[UUID, AppWeaponProperty] = {}

    async def name_exists(self, name: str) -> bool:
        return any(
            weapon_property.name == name for weapon_property in self._store.values()
        )

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, weapon_property_id: UUID) -> bool:
        return weapon_property_id in self._store

    async def get_by_id(self, weapon_property_id: UUID) -> AppWeaponProperty:
        return self._store[weapon_property_id]

    async def get_all(self) -> list[AppWeaponProperty]:
        return list(self._store.values())

    async def filter(
        self, search_by_name: str | None = None
    ) -> list[AppWeaponProperty]:
        if search_by_name is not None:
            return [w for w in self._store.values() if search_by_name in w.name]
        return list(self._store.values())

    async def save(self, weapon_property: AppWeaponProperty) -> None:
        self._store[weapon_property.weapon_property_id] = weapon_property

    async def delete(self, weapon_property_id: UUID) -> None:
        del self._store[weapon_property_id]
