from domain.tool.repository import ToolRepository


class ToolService:
    def __init__(self, tool_repository: ToolRepository) -> None:
        self.__repository = tool_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
