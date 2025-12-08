from uuid import UUID, uuid4

from application.dto.model.subclass_feature import AppSubclassFeature
from application.repository import (
    SubclassFeatureRepository as AppSubclassFeatureRepository,
)
from domain.subclass_feature import (
    SubclassFeatureRepository as DomainSubclassFeatureRepository,
)


class InMemorySubclassFeatureRepository(
    DomainSubclassFeatureRepository, AppSubclassFeatureRepository
):
    def __init__(self) -> None:
        self._store: dict[UUID, AppSubclassFeature] = {}

    async def name_for_class_exists(self, subclass_id: UUID, name: str) -> bool:
        return any(
            feature.name == name and feature.subclass_id == subclass_id
            for feature in self._store.values()
        )

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, feature_id: UUID) -> bool:
        return feature_id in self._store

    async def get_by_id(self, feature_id: UUID) -> AppSubclassFeature:
        return self._store[feature_id]

    async def get_all(self) -> list[AppSubclassFeature]:
        return list(self._store.values())

    async def filter(
        self, filter_by_subclass_id: UUID | None = None
    ) -> list[AppSubclassFeature]:
        if filter_by_subclass_id is not None:
            return [
                f
                for f in self._store.values()
                if f.subclass_id == filter_by_subclass_id
            ]
        return list(self._store.values())

    async def create(self, feature: AppSubclassFeature) -> None:
        self._store[feature.feature_id] = feature

    async def update(self, feature: AppSubclassFeature) -> None:
        self._store[feature.feature_id] = feature

    async def delete(self, feature_id: UUID) -> None:
        del self._store[feature_id]
