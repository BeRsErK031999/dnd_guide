from dataclasses import dataclass
from uuid import UUID

__all__ = ["SpellQuery", "SpellsQuery"]


@dataclass
class SpellQuery:
    spell_id: UUID


@dataclass
class SpellsQuery:
    search_by_name: str | None = None
    filter_by_class_ids: list[UUID] | None = None
    filter_by_subclass_ids: list[UUID] | None = None
    filter_by_schools: list[str] | None = None
    filter_by_damage_types: list[str] | None = None
    filter_by_durations: list[str] | None = None
    filter_by_casting_times: list[str] | None = None
    filter_by_verbal_component: bool | None = None
    filter_by_symbolic_component: bool | None = None
    filter_by_material_component: bool | None = None
    filter_by_concentration: bool | None = None
    filter_by_ritual: bool | None = None
    filter_by_source_ids: list[UUID] | None = None
