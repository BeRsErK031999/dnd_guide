from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.tool import AppTool


class ToolRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, tool_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, tool_id: UUID) -> AppTool:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppTool]:
        raise NotImplemented

    @abstractmethod
    async def filter(self, search_by_name: str | None = None) -> list[AppTool]:
        raise NotImplemented

    @abstractmethod
    async def save(self, tool: AppTool) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, tool_id: UUID) -> None:
        raise NotImplemented
