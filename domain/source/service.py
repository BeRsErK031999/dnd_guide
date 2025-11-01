from domain.source.repository import SourceRepository


class SourceService:
    def __init__(self, source_repository: SourceRepository) -> None:
        self.__repository = source_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
