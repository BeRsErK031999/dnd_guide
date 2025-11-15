from application.dto.query.feat import FeatQuery
from application.repository import FeatRepository
from domain.error import DomainError
from domain.feat import Feat


class GetFeatUseCase:
    def __init__(self, feat_repository: FeatRepository):
        self.__repository = feat_repository

    async def execute(self, query: FeatQuery) -> Feat:
        if not await self.__repository.id_exists(query.feat_id):
            raise DomainError.not_found(f"черты с id {query.feat_id} не существует")
        return await self.__repository.get_by_id(query.feat_id)
