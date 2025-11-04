from abc import ABC, abstractmethod
from uuid import UUID

from domain.subclass_feature.feature import SubclassFeature


class SubclassFeatureRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_feature_of_id_exist(self, feature_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_feature_of_id(self, feature_id: UUID) -> SubclassFeature:
        raise NotImplemented

    @abstractmethod
    async def save(self, feature: SubclassFeature) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, feature_id: UUID) -> None:
        raise NotImplemented
