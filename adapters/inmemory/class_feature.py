from uuid import UUID, uuid4

from application.repository import ClassFeatureRepository as AppClassFeatureRepository
from domain.class_feature import ClassFeature
from domain.class_feature import ClassFeatureRepository as DomainClassFeatureRepository


class InMemoryClassFeatureRepository(
    DomainClassFeatureRepository, AppClassFeatureRepository
):
    def __init__(self) -> None:
        self.__store: dict[UUID, ClassFeature] = {}

    async def is_name_exist(self, name: str) -> bool:
        return any(feature.name == name for feature in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def is_feature_of_id_exist(self, feature_id: UUID) -> bool:
        return feature_id in self.__store

    async def get_feature_of_id(self, feature_id: UUID) -> ClassFeature:
        return self.__store[feature_id]

    async def save(self, feature: ClassFeature) -> None:
        self.__store[feature.feature_id()] = feature

    async def delete(self, feature_id: UUID) -> None:
        del self.__store[feature_id]
