from application.dto.query.subclass_feature import SubclassFeaturesQuery
from application.repository import SubclassFeatureRepository
from domain.subclass_feature import SubclassFeature


class GetSubclassFeaturesUseCase:
    def __init__(self, feature_repository: SubclassFeatureRepository):
        self.__repository = feature_repository

    async def execute(self, query: SubclassFeaturesQuery) -> list[SubclassFeature]:
        return await self.__repository.filter(
            filter_by_subclass_id=query.filter_by_subclass_id
        )
