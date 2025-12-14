from application.dto.model.subclass_feature import AppSubclassFeature
from application.dto.query.subclass_feature import SubclassFeaturesQuery
from application.repository import SubclassFeatureRepository


class GetSubclassFeaturesUseCase:
    def __init__(self, feature_repository: SubclassFeatureRepository):
        self._repository = feature_repository

    async def execute(self, query: SubclassFeaturesQuery) -> list[AppSubclassFeature]:
        return await self._repository.filter(
            filter_by_subclass_id=query.filter_by_subclass_id
        )
