from abc import ABC, abstractmethod
from uuid import UUID

from domain.weapon_kind import WeaponKind


class WeaponKindRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, weapon_kind_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, weapon_kind_id: UUID) -> WeaponKind:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[WeaponKind]:
        raise NotImplemented

    @abstractmethod
    async def create(self, weapon_kind: WeaponKind) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, weapon_kind: WeaponKind) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, weapon_kind_id: UUID) -> None:
        raise NotImplemented
