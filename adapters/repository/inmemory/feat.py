from uuid import UUID, uuid4

from application.repository import FeatRepository as AppFeatRepository
from domain.feat import FeatRepository as DomainFeatRepository
from domain.feat.feat import Feat


class InMemoryFeatRepository(DomainFeatRepository, AppFeatRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, Feat] = {}

    async def is_name_exist(self, name: str) -> bool:
        return any(feat.name == name for feat in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def is_feat_of_id_exist(self, feat_id: UUID) -> bool:
        return feat_id in self.__store

    async def get_feat_of_id(self, feat_id: UUID) -> Feat:
        return self.__store[feat_id]

    async def save(self, feat: Feat) -> None:
        self.__store[feat.feat_id()] = feat

    async def delete(self, feat_id: UUID) -> None:
        del self.__store[feat_id]
