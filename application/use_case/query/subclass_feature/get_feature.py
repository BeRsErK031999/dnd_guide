from application.dto.query.subclass_feature import SubclassFeatureQuery
from application.repository import SubclassFeatureRepository
from domain.error import DomainError
from domain.subclass_feature import SubclassFeature


class GetSubclassFeatureUseCase:
    def __init__(self, feature_repository: SubclassFeatureRepository):
        self.__repository = feature_repository

    async def execute(self, query: SubclassFeatureQuery) -> SubclassFeature:
        if not await self.__repository.id_exists(query.feature_id):
            raise DomainError.not_found(f"умения с id {query.feature_id} не существует")
        return await self.__repository.get_by_id(query.feature_id)
