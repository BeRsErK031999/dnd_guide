from uuid import UUID

from domain.class_feature.repository import ClassFeatureRepository


class ClassFeatureService:
    def __init__(self, class_feature_repository: ClassFeatureRepository) -> None:
        self.__repository = class_feature_repository

    async def can_create_for_class_with_name(self, class_id: UUID, name: str) -> bool:
        return await self.__repository.is_name_for_class_exist(class_id, name)

    async def can_rename_for_class_with_name(self, class_id: UUID, name: str) -> bool:
        return await self.__repository.is_name_for_class_exist(class_id, name)
