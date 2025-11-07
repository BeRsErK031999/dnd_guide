from uuid import UUID, uuid4

from application.repository import ToolRepository as AppToolRepository
from domain.tool import Tool
from domain.tool import ToolRepository as DomainToolRepository


class InMemoryToolRepository(DomainToolRepository, AppToolRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, Tool] = {}

    async def is_name_exist(self, name: str) -> bool:
        return any(tool.name == name for tool in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def is_tool_of_id_exist(self, tool_id: UUID) -> bool:
        return tool_id in self.__store

    async def get_tool_of_id(self, tool_id: UUID) -> Tool:
        return self.__store[tool_id]

    async def save(self, tool: Tool) -> None:
        self.__store[tool.tool_id()] = tool

    async def delete(self, tool_id: UUID) -> None:
        del self.__store[tool_id]
