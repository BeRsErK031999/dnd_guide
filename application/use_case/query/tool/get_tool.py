from application.dto.query.tool import ToolQuery
from application.repository import ToolRepository
from domain.error import DomainError
from domain.tool import Tool


class GetToolUseCase:
    def __init__(self, tool_repository: ToolRepository):
        self.__repository = tool_repository

    async def execute(self, query: ToolQuery) -> Tool:
        if not await self.__repository.id_exists(query.tool_id):
            raise DomainError.not_found(
                f"инструмента с id {query.tool_id} не существует"
            )
        return await self.__repository.get_by_id(query.tool_id)
