from abc import ABC, abstractmethod
from uuid import UUID

from domain.armor import Armor


class ArmorRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, armor_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, armor_id: UUID) -> Armor:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Armor]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_armor_type: list[str] | None = None,
        filter_by_material_id: list[UUID] | None = None,
    ) -> list[Armor]:
        raise NotImplemented

    @abstractmethod
    async def create(self, armor: Armor) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, armor: Armor) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, armor_id: UUID) -> None:
        raise NotImplemented
