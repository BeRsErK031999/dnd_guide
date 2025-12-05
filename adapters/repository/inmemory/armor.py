from uuid import UUID, uuid4

from application.dto.model.armor import AppArmor
from application.repository import ArmorRepository as AppArmorRepository
from domain.armor import Armor
from domain.armor import ArmorRepository as DomainArmorRepository


class InMemoryArmorRepository(DomainArmorRepository, AppArmorRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, AppArmor] = {}

    async def name_exists(self, name: str) -> bool:
        return any(armor.name == name for armor in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, armor_id: UUID) -> bool:
        return armor_id in self.__store

    async def get_by_id(self, armor_id: UUID) -> AppArmor:
        return self.__store[armor_id]

    async def get_all(self) -> list[AppArmor]:
        return list(self.__store.values())

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_armor_types: list[str] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> list[AppArmor]:
        return await self.get_all()

    async def create(self, armor: AppArmor) -> None:
        self.__store[armor.armor_id] = armor

    async def update(self, armor: AppArmor) -> None:
        self.__store[armor.armor_id] = armor

    async def delete(self, armor_id: UUID) -> None:
        del self.__store[armor_id]
