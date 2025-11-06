from domain.feat.repository import FeatRepository


class FeatService:
    def __init__(self, feat_repository: FeatRepository) -> None:
        self.__repository = feat_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
