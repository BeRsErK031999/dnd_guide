from application.dto.query.class_feature import ClassFeaturesQuery
from application.repository import ClassFeatureRepository
from domain.class_feature import ClassFeature


class GetClassFeaturesUseCase:
    def __init__(self, feature_repository: ClassFeatureRepository):
        self.__repository = feature_repository

    async def execute(self, query: ClassFeaturesQuery) -> list[ClassFeature]:
        return await self.__repository.filter(
            filter_by_class_id=query.filter_by_class_id
        )
