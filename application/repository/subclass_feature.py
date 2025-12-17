from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.subclass_feature import AppSubclassFeature


class SubclassFeatureRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, feature_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, feature_id: UUID) -> AppSubclassFeature:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppSubclassFeature]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self, filter_by_subclass_id: UUID | None = None
    ) -> list[AppSubclassFeature]:
        raise NotImplemented

    @abstractmethod
    async def save(self, feature: AppSubclassFeature) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, feature_id: UUID) -> None:
        raise NotImplemented
