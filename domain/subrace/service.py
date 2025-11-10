from domain.subrace.repository import SubraceRepository


class SubraceService:
    def __init__(self, subrace_repository: SubraceRepository) -> None:
        self.__repository = subrace_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)
