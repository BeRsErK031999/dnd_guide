from abc import ABC, abstractmethod
from uuid import UUID

from domain.class_feature.feature import ClassFeature


class ClassFeatureRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_feature_of_id_exist(self, feature_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_feature_of_id(self, feature_id: UUID) -> ClassFeature:
        raise NotImplemented

    @abstractmethod
    async def save(self, feature: ClassFeature) -> None:
        raise NotImplemented
