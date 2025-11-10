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
    async def save(self, feat: Feat) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, feat_id: UUID) -> None:
        raise NotImplemented
