from dataclasses import dataclass
from uuid import UUID

__all__ = ["FeatQuery", "FeatsQuery"]


@dataclass
class FeatQuery:
    feat_id: UUID


@dataclass
class FeatsQuery:
    search_by_name: str | None = None
    filter_by_caster: bool | None = None
    filter_by_required_armor_types: list[str] | None = None
    filter_by_required_modifiers: list[str] | None = None
    filter_by_increase_modifiers: list[str] | None = None
