from domain.tool.repository import ToolRepository


class ToolService:
    def __init__(self, tool_repository: ToolRepository) -> None:
        self._repository = tool_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)
