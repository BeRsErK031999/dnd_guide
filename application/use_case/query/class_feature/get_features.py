from application.dto.model.class_feature import AppClassFeature
from application.dto.query.class_feature import ClassFeaturesQuery
from application.repository import ClassFeatureRepository


class GetClassFeaturesUseCase:
    def __init__(self, feature_repository: ClassFeatureRepository):
        self.__repository = feature_repository

    async def execute(self, query: ClassFeaturesQuery) -> list[AppClassFeature]:
        return await self.__repository.filter(
            filter_by_class_id=query.filter_by_class_id
        )
