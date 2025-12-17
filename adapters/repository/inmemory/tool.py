from uuid import UUID, uuid4

from application.dto.model.tool import AppTool
from application.repository import ToolRepository as AppToolRepository
from domain.tool import ToolRepository as DomainToolRepository


class InMemoryToolRepository(DomainToolRepository, AppToolRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppTool] = {}

    async def name_exists(self, name: str) -> bool:
        return any(tool.name == name for tool in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, tool_id: UUID) -> bool:
        return tool_id in self._store

    async def get_by_id(self, tool_id: UUID) -> AppTool:
        return self._store[tool_id]

    async def get_all(self) -> list[AppTool]:
        return list(self._store.values())

    async def filter(self, search_by_name: str | None = None) -> list[AppTool]:
        if search_by_name is not None:
            return [t for t in self._store.values() if search_by_name in t.name]
        return list(self._store.values())

    async def save(self, tool: AppTool) -> None:
        self._store[tool.tool_id] = tool

    async def delete(self, tool_id: UUID) -> None:
        del self._store[tool_id]
