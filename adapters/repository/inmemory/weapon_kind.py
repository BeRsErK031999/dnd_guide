from uuid import UUID, uuid4

from application.repository import WeaponKindRepository as AppWeaponKindRepository
from domain.weapon_kind import WeaponKind
from domain.weapon_kind import WeaponKindRepository as DomainWeaponKindRepository


class InMemoryWeaponKindRepository(DomainWeaponKindRepository, AppWeaponKindRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, WeaponKind] = {}

    async def name_exists(self, name: str) -> bool:
        return any(weapon_kind.name() == name for weapon_kind in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, weapon_kind_id: UUID) -> bool:
        return weapon_kind_id in self.__store

    async def get_by_id(self, weapon_kind_id: UUID) -> WeaponKind:
        return self.__store[weapon_kind_id]

    async def get_all(self) -> list[WeaponKind]:
        return list(self.__store.values())

    async def create(self, weapon_kind: WeaponKind) -> None:
        self.__store[weapon_kind.weapon_kind_id()] = weapon_kind

    async def update(self, weapon_kind: WeaponKind) -> None:
        self.__store[weapon_kind.weapon_kind_id()] = weapon_kind

    async def delete(self, weapon_kind_id: UUID) -> None:
        del self.__store[weapon_kind_id]
