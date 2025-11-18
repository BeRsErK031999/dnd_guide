from abc import ABC, abstractmethod
from uuid import UUID

from domain.tool import Tool


class ToolRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, tool_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, tool_id: UUID) -> Tool:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Tool]:
        raise NotImplemented

    @abstractmethod
    async def filter(self, search_by_name: str | None = None) -> list[Tool]:
        raise NotImplemented

    @abstractmethod
    async def create(self, tool: Tool) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, tool: Tool) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, tool_id: UUID) -> None:
        raise NotImplemented
