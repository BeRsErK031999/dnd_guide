from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.weapon_kind import AppWeaponKind


class WeaponKindRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, weapon_kind_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, weapon_kind_id: UUID) -> AppWeaponKind:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppWeaponKind]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_types: list[str] | None = None,
    ) -> list[AppWeaponKind]:
        raise NotImplemented

    @abstractmethod
    async def save(self, weapon_kind: AppWeaponKind) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, weapon_kind_id: UUID) -> None:
        raise NotImplemented
