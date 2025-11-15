from application.repository import ClassFeatureRepository
from domain.class_feature import ClassFeature


class GetClassFeaturesUseCase:
    def __init__(self, class_feature_repository: ClassFeatureRepository):
        self.__repository = class_feature_repository

    async def execute(self) -> list[ClassFeature]:
        return await self.__repository.get_all()
