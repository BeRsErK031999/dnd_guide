from uuid import UUID

from domain.subclass_feature.repository import SubclassFeatureRepository


class SubclassFeatureService:
    def __init__(self, subclass_feature_repository: SubclassFeatureRepository) -> None:
        self._repository = subclass_feature_repository

    async def can_create_for_subclass_with_name(
        self, subclass_id: UUID, name: str
    ) -> bool:
        return not await self._repository.name_for_subclass_exists(subclass_id, name)

    async def can_rename_for_subclass_with_name(
        self, subclass_id: UUID, name: str
    ) -> bool:
        return not await self._repository.name_for_subclass_exists(subclass_id, name)
