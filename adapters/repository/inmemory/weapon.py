from uuid import UUID, uuid4

from application.dto.model.weapon import AppWeapon
from application.repository import WeaponRepository as AppWeaponRepository
from domain.weapon import WeaponRepository as DomainWeaponRepository


class InMemoryWeaponRepository(DomainWeaponRepository, AppWeaponRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppWeapon] = {}

    async def name_exists(self, name: str) -> bool:
        return any(weapon.name == name for weapon in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, weapon_id: UUID) -> bool:
        return weapon_id in self._store

    async def get_by_id(self, weapon_id: UUID) -> AppWeapon:
        return self._store[weapon_id]

    async def get_all(self) -> list[AppWeapon]:
        return list(self._store.values())

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_kind_ids: list[UUID] | None = None,
        filter_by_damage_types: list[str] | None = None,
        filter_by_property_ids: list[UUID] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> list[AppWeapon]:
        result: list[AppWeapon] = list()
        for w in self._store.values():
            if (
                (search_by_name is None or search_by_name in w.name)
                and (
                    filter_by_kind_ids is None or w.weapon_kind_id in filter_by_kind_ids
                )
                and (
                    filter_by_damage_types is None
                    or w.damage.damage_type in filter_by_damage_types
                )
                and (
                    filter_by_property_ids is None
                    or any(p in filter_by_property_ids for p in w.weapon_property_ids)
                )
                and (
                    filter_by_material_ids is None
                    or w.material_id in filter_by_material_ids
                )
            ):
                result.append(w)
        return result

    async def save(self, weapon: AppWeapon) -> None:
        self._store[weapon.weapon_id] = weapon

    async def delete(self, weapon_id: UUID) -> None:
        del self._store[weapon_id]
