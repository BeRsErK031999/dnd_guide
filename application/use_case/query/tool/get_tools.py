from application.repository import ToolRepository
from domain.tool import Tool


class GetToolsUseCase:
    def __init__(self, tool_repository: ToolRepository):
        self.__repository = tool_repository

    async def execute(self) -> list[Tool]:
        return await self.__repository.get_all()
