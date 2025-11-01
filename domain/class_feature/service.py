from domain.class_feature.repository import ClassFeatureRepository


class ClassFeatureService:
    def __init__(self, class_feature_repository: ClassFeatureRepository) -> None:
        self.__repository = class_feature_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
