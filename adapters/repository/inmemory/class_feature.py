from uuid import UUID, uuid4

from application.dto.model.class_feature import AppClassFeature
from application.repository import ClassFeatureRepository as AppClassFeatureRepository
from domain.class_feature import ClassFeatureRepository as DomainClassFeatureRepository


class InMemoryClassFeatureRepository(
    DomainClassFeatureRepository, AppClassFeatureRepository
):
    def __init__(self) -> None:
        self._store: dict[UUID, AppClassFeature] = {}

    async def name_for_class_exists(self, class_id: UUID, name: str) -> bool:
        return any(feature.name == name for feature in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, feature_id: UUID) -> bool:
        return feature_id in self._store

    async def get_by_id(self, feature_id: UUID) -> AppClassFeature:
        return self._store[feature_id]

    async def get_all(self) -> list[AppClassFeature]:
        return list(self._store.values())

    async def filter(
        self, filter_by_class_id: UUID | None = None
    ) -> list[AppClassFeature]:
        if filter_by_class_id is not None:
            return [f for f in self._store.values() if f.class_id == filter_by_class_id]
        return list(self._store.values())

    async def create(self, feature: AppClassFeature) -> None:
        self._store[feature.feature_id] = feature

    async def update(self, feature: AppClassFeature) -> None:
        self._store[feature.feature_id] = feature

    async def delete(self, feature_id: UUID) -> None:
        del self._store[feature_id]
