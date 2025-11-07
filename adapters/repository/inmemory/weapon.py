from uuid import UUID, uuid4

from application.repository import WeaponRepository as AppWeaponRepository
from domain.weapon import Weapon
from domain.weapon import WeaponRepository as DomainWeaponRepository


class InMemoryWeaponRepository(DomainWeaponRepository, AppWeaponRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, Weapon] = {}

    async def is_name_exist(self, name: str) -> bool:
        return any(weapon.name == name for weapon in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def is_weapon_of_id_exist(self, weapon_id: UUID) -> bool:
        return weapon_id in self.__store

    async def get_weapon_of_id(self, weapon_id: UUID) -> Weapon:
        return self.__store[weapon_id]

    async def save(self, weapon: Weapon) -> None:
        self.__store[weapon.weapon_id()] = weapon

    async def delete(self, weapon_id: UUID) -> None:
        del self.__store[weapon_id]
