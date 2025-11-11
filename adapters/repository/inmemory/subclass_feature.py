from uuid import UUID, uuid4

from application.repository import (
    SubclassFeatureRepository as AppSubclassFeatureRepository,
)
from domain.subclass_feature import SubclassFeature
from domain.subclass_feature import (
    SubclassFeatureRepository as DomainSubclassFeatureRepository,
)


class InMemorySubclassFeatureRepository(
    DomainSubclassFeatureRepository, AppSubclassFeatureRepository
):
    def __init__(self) -> None:
        self.__store: dict[UUID, SubclassFeature] = {}

    async def name_exists(self, name: str) -> bool:
        return any(feature.name() == name for feature in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, feature_id: UUID) -> bool:
        return feature_id in self.__store

    async def get_by_id(self, feature_id: UUID) -> SubclassFeature:
        return self.__store[feature_id]

    async def get_all(self) -> list[SubclassFeature]:
        return list(self.__store.values())

    async def create(self, feature: SubclassFeature) -> None:
        self.__store[feature.feature_id()] = feature

    async def update(self, feature: SubclassFeature) -> None:
        self.__store[feature.feature_id()] = feature

    async def delete(self, feature_id: UUID) -> None:
        del self.__store[feature_id]
