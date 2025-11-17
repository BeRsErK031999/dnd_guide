from abc import ABC, abstractmethod
from uuid import UUID

from domain.class_feature import ClassFeature


class ClassFeatureRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, feature_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, feature_id: UUID) -> ClassFeature:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[ClassFeature]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self, filter_by_class_id: UUID | None = None
    ) -> list[ClassFeature]:
        raise NotImplemented

    @abstractmethod
    async def create(self, feature: ClassFeature) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, feature: ClassFeature) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, feature_id: UUID) -> None:
        raise NotImplemented
