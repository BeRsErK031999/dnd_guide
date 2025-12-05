from application.dto.model.tool import AppTool
from application.dto.query.tool import ToolsQuery
from application.repository import ToolRepository


class GetToolsUseCase:
    def __init__(self, tool_repository: ToolRepository):
        self.__repository = tool_repository

    async def execute(self, query: ToolsQuery) -> list[AppTool]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
