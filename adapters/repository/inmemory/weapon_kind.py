from uuid import UUID, uuid4

from application.dto.model.weapon_kind import AppWeaponKind
from application.repository import WeaponKindRepository as AppWeaponKindRepository
from domain.weapon_kind import WeaponKindRepository as DomainWeaponKindRepository


class InMemoryWeaponKindRepository(DomainWeaponKindRepository, AppWeaponKindRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppWeaponKind] = {}

    async def name_exists(self, name: str) -> bool:
        return any(weapon_kind.name == name for weapon_kind in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, weapon_kind_id: UUID) -> bool:
        return weapon_kind_id in self._store

    async def get_by_id(self, weapon_kind_id: UUID) -> AppWeaponKind:
        return self._store[weapon_kind_id]

    async def get_all(self) -> list[AppWeaponKind]:
        return list(self._store.values())

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_types: list[str] | None = None,
    ) -> list[AppWeaponKind]:
        result: list[AppWeaponKind] = list()
        for k in self._store.values():
            if (search_by_name is None or search_by_name in k.name) and (
                filter_by_types is None or k.weapon_type in filter_by_types
            ):
                result.append(k)
        return result

    async def save(self, weapon_kind: AppWeaponKind) -> None:
        self._store[weapon_kind.weapon_kind_id] = weapon_kind

    async def delete(self, weapon_kind_id: UUID) -> None:
        del self._store[weapon_kind_id]
