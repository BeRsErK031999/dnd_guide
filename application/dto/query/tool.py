from dataclasses import dataclass
from uuid import UUID


@dataclass
class ToolQuery:
    tool_id: UUID


@dataclass
class ToolsQuery:
    search_by_name: str | None = None
