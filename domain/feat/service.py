from domain.feat.repository import FeatRepository


class FeatService:
    def __init__(self, feat_repository: FeatRepository) -> None:
        self.__repository = feat_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)
