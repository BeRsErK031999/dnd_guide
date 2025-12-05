from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.weapon import AppWeapon


class WeaponRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, weapon_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, weapon_id: UUID) -> AppWeapon:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppWeapon]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_kind_ids: list[UUID] | None = None,
        filter_by_damage_types: list[str] | None = None,
        filter_by_property_ids: list[UUID] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> list[AppWeapon]:
        raise NotImplemented

    @abstractmethod
    async def create(self, weapon: AppWeapon) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, weapon: AppWeapon) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, weapon_id: UUID) -> None:
        raise NotImplemented
