from application.dto.model.tool import AppTool
from application.dto.query.tool import ToolQuery
from application.repository import ToolRepository
from domain.error import DomainError


class GetToolUseCase:
    def __init__(self, tool_repository: ToolRepository):
        self._tool_repository = tool_repository

    async def execute(self, query: ToolQuery) -> AppTool:
        if not await self._tool_repository.id_exists(query.tool_id):
            raise DomainError.not_found(
                f"инструмента с id {query.tool_id} не существует"
            )
        return await self._tool_repository.get_by_id(query.tool_id)
