from uuid import UUID, uuid4

from application.dto.model.feat import AppFeat
from application.repository import FeatRepository as AppFeatRepository
from domain.feat import FeatRepository as DomainFeatRepository


class InMemoryFeatRepository(DomainFeatRepository, AppFeatRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppFeat] = {}

    async def name_exists(self, name: str) -> bool:
        return any(feat.name == name for feat in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, feat_id: UUID) -> bool:
        return feat_id in self._store

    async def get_by_id(self, feat_id: UUID) -> AppFeat:
        return self._store[feat_id]

    async def get_all(self) -> list[AppFeat]:
        return list(self._store.values())

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_caster: bool | None = None,
        filter_by_required_armor_types: list[str] | None = None,
        filter_by_required_modifiers: list[str] | None = None,
        filter_by_increase_modifiers: list[str] | None = None,
    ) -> list[AppFeat]:
        result: list[AppFeat] = list()
        for f in self._store.values():
            if (
                (search_by_name is None or search_by_name in f.name)
                and (filter_by_caster is None or filter_by_caster == f.caster)
                and (
                    filter_by_required_modifiers is None
                    or all(
                        m in f.required_modifiers for m in filter_by_required_modifiers
                    )
                )
                and (
                    filter_by_required_armor_types is None
                    or all(
                        a in f.required_armor_types
                        for a in filter_by_required_armor_types
                    )
                )
                and (
                    filter_by_increase_modifiers is None
                    or all(
                        m in f.increase_modifiers for m in filter_by_increase_modifiers
                    )
                )
            ):
                result.append(f)
        return result

    async def create(self, feat: AppFeat) -> None:
        self._store[feat.feat_id] = feat

    async def update(self, feat: AppFeat) -> None:
        self._store[feat.feat_id] = feat

    async def delete(self, feat_id: UUID) -> None:
        del self._store[feat_id]
