from uuid import UUID, uuid4

from application.repository import (
    WeaponPropertyRepository as AppWeaponPropertyRepository,
)
from domain.weapon_property import WeaponProperty
from domain.weapon_property import (
    WeaponPropertyRepository as DomainWeaponPropertyRepository,
)


class InMemoryWeaponPropertyRepository(
    DomainWeaponPropertyRepository, AppWeaponPropertyRepository
):
    def __init__(self) -> None:
        self.__store: dict[UUID, WeaponProperty] = {}

    async def name_exists(self, name: str) -> bool:
        return any(
            weapon_property.name == name for weapon_property in self.__store.values()
        )

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, weapon_property_id: UUID) -> bool:
        return weapon_property_id in self.__store

    async def get_by_id(self, weapon_property_id: UUID) -> WeaponProperty:
        return self.__store[weapon_property_id]

    async def save(self, weapon_property: WeaponProperty) -> None:
        self.__store[weapon_property.weapon_property_id()] = weapon_property

    async def delete(self, weapon_property_id: UUID) -> None:
        del self.__store[weapon_property_id]
