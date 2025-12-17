from uuid import UUID, uuid4

from application.dto.model.armor import AppArmor
from application.repository import ArmorRepository as AppArmorRepository
from domain.armor import ArmorRepository as DomainArmorRepository


class InMemoryArmorRepository(DomainArmorRepository, AppArmorRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppArmor] = {}

    async def name_exists(self, name: str) -> bool:
        return any(armor.name == name for armor in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, armor_id: UUID) -> bool:
        return armor_id in self._store

    async def get_by_id(self, armor_id: UUID) -> AppArmor:
        return self._store[armor_id]

    async def get_all(self) -> list[AppArmor]:
        return list(self._store.values())

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_armor_types: list[str] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> list[AppArmor]:
        result: list[AppArmor] = list()
        for armor in self._store.values():
            if (
                (search_by_name is None or search_by_name in armor.name)
                and (
                    filter_by_armor_types is None
                    or armor.armor_type in filter_by_armor_types
                )
                and (
                    filter_by_material_ids is None
                    or armor.material_id in filter_by_material_ids
                )
            ):
                result.append(armor)
        return result

    async def save(self, armor: AppArmor) -> None:
        self._store[armor.armor_id] = armor

    async def delete(self, armor_id: UUID) -> None:
        del self._store[armor_id]
