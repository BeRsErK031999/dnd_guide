from domain.subrace.repository import SubraceRepository


class SubraceService:
    def __init__(self, subrace_repository: SubraceRepository) -> None:
        self.__repository = subrace_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
