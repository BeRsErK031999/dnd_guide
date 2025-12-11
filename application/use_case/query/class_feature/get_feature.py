from application.dto.model.class_feature import AppClassFeature
from application.dto.query.class_feature import ClassFeatureQuery
from application.repository import ClassFeatureRepository
from domain.error import DomainError


class GetClassFeatureUseCase:
    def __init__(self, feature_repository: ClassFeatureRepository):
        self._repository = feature_repository

    async def execute(self, query: ClassFeatureQuery) -> AppClassFeature:
        if not await self._repository.id_exists(query.feature_id):
            raise DomainError.not_found(
                f"умения класса с id {query.feature_id} не существует"
            )
        return await self._repository.get_by_id(query.feature_id)
