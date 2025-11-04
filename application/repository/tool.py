from abc import ABC, abstractmethod
from uuid import UUID

from domain.tool.tool import Tool


class ToolRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_tool_of_id_exist(self, tool_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_tool_of_id(self, tool_id: UUID) -> Tool:
        raise NotImplemented

    @abstractmethod
    async def save(self, tool: Tool) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, tool_id: UUID) -> None:
        raise NotImplemented
