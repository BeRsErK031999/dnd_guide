from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.feat import AppFeat


class FeatRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, feat_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, feat_id: UUID) -> AppFeat:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppFeat]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_caster: bool | None = None,
        filter_by_required_armor_types: list[str] | None = None,
        filter_by_required_modifiers: list[str] | None = None,
        filter_by_increase_modifiers: list[str] | None = None,
    ) -> list[AppFeat]:
        raise NotImplemented

    @abstractmethod
    async def save(self, feat: AppFeat) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, feat_id: UUID) -> None:
        raise NotImplemented
