from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.armor import AppArmor


class ArmorRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, armor_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, armor_id: UUID) -> AppArmor:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppArmor]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_armor_types: list[str] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> list[AppArmor]:
        raise NotImplemented

    @abstractmethod
    async def create(self, armor: AppArmor) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, armor: AppArmor) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, armor_id: UUID) -> None:
        raise NotImplemented
