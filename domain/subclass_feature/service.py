from uuid import UUID

from domain.subclass_feature.repository import SubclassFeatureRepository


class SubclassFeatureService:
    def __init__(self, subclass_feature_repository: SubclassFeatureRepository) -> None:
        self.__repository = subclass_feature_repository

    async def can_create_for_class_with_name(
        self, subclass_id: UUID, name: str
    ) -> bool:
        return await self.__repository.name_for_class_exists(subclass_id, name)

    async def can_rename_for_class_with_name(
        self, subclass_id: UUID, name: str
    ) -> bool:
        return await self.__repository.name_for_class_exists(subclass_id, name)
