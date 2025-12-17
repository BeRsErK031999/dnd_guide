from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.weapon_property import AppWeaponProperty


class WeaponPropertyRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, weapon_property_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, weapon_property_id: UUID) -> AppWeaponProperty:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppWeaponProperty]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self, search_by_name: str | None = None
    ) -> list[AppWeaponProperty]:
        raise NotImplemented

    @abstractmethod
    async def save(self, weapon_property: AppWeaponProperty) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, weapon_property_id: UUID) -> None:
        raise NotImplemented
