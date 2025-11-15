from application.repository import SubclassFeatureRepository
from domain.subclass_feature import SubclassFeature


class GetSubclassFeaturesUseCase:
    def __init__(self, feature_repository: SubclassFeatureRepository):
        self.__repository = feature_repository

    async def execute(self) -> list[SubclassFeature]:
        return await self.__repository.get_all()
