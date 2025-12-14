from application.dto.model.subclass_feature import AppSubclassFeature
from application.dto.query.subclass_feature import SubclassFeatureQuery
from application.repository import SubclassFeatureRepository
from domain.error import DomainError


class GetSubclassFeatureUseCase:
    def __init__(self, feature_repository: SubclassFeatureRepository):
        self._repository = feature_repository

    async def execute(self, query: SubclassFeatureQuery) -> AppSubclassFeature:
        if not await self._repository.id_exists(query.feature_id):
            raise DomainError.not_found(f"умения с id {query.feature_id} не существует")
        return await self._repository.get_by_id(query.feature_id)
