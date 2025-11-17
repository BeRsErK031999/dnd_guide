from abc import ABC, abstractmethod
from uuid import UUID

from domain.feat import Feat


class FeatRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, feat_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, feat_id: UUID) -> Feat:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Feat]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_caster: bool | None = None,
        filter_by_required_armor_types: list[str] | None = None,
        filter_by_required_modifiers: list[str] | None = None,
        filter_by_increase_modifiers: list[str] | None = None,
    ) -> list[Feat]:
        raise NotImplemented

    @abstractmethod
    async def create(self, feat: Feat) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, feat: Feat) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, feat_id: UUID) -> None:
        raise NotImplemented
