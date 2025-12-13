from application.dto.model.feat import AppFeat
from application.dto.query.feat import FeatQuery
from application.repository import FeatRepository
from domain.error import DomainError


class GetFeatUseCase:
    def __init__(self, feat_repository: FeatRepository):
        self._repository = feat_repository

    async def execute(self, query: FeatQuery) -> AppFeat:
        if not await self._repository.id_exists(query.feat_id):
            raise DomainError.not_found(f"черты с id {query.feat_id} не существует")
        return await self._repository.get_by_id(query.feat_id)
