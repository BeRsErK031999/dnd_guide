from application.dto.model.tool import AppTool
from application.dto.query.tool import ToolsQuery
from application.repository import ToolRepository


class GetToolsUseCase:
    def __init__(self, tool_repository: ToolRepository):
        self._tool_repository = tool_repository

    async def execute(self, query: ToolsQuery) -> list[AppTool]:
        return await self._tool_repository.filter(search_by_name=query.search_by_name)
