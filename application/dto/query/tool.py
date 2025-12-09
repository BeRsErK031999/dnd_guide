from dataclasses import dataclass
from uuid import UUID

__all__ = ["ToolQuery", "ToolsQuery"]


@dataclass
class ToolQuery:
    tool_id: UUID


@dataclass
class ToolsQuery:
    search_by_name: str | None = None
