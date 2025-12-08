from uuid import UUID, uuid4

from application.dto.model.spell import AppSpell
from application.repository import SpellRepository as AppSpellRepository
from domain.spell import SpellRepository as DomainSpellRepository


class InMemorySpellRepository(DomainSpellRepository, AppSpellRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppSpell] = {}

    async def name_exists(self, name: str) -> bool:
        return any(spell.name == name for spell in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, spell_id: UUID) -> bool:
        return spell_id in self._store

    async def get_by_id(self, spell_id: UUID) -> AppSpell:
        return self._store[spell_id]

    async def get_all(self) -> list[AppSpell]:
        return list(self._store.values())

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_class_ids: list[UUID] | None = None,
        filter_by_subclass_ids: list[UUID] | None = None,
        filter_by_schools: list[str] | None = None,
        filter_by_damage_types: list[str] | None = None,
        filter_by_durations: list[str] | None = None,
        filter_by_casting_times: list[str] | None = None,
        filter_by_verbal_component: bool | None = None,
        filter_by_symbolic_component: bool | None = None,
        filter_by_material_component: bool | None = None,
        filter_by_concentration: bool | None = None,
        filter_by_ritual: bool | None = None,
        filter_by_source_ids: list[UUID] | None = None,
    ) -> list[AppSpell]:
        result: list[AppSpell] = list()
        for s in self._store.values():
            if (
                (search_by_name is None or search_by_name in s.name)
                and (
                    filter_by_class_ids is None
                    or any(c in s.class_ids for c in filter_by_class_ids)
                )
                and (
                    filter_by_subclass_ids is None
                    or any(c in s.subclass_ids for c in filter_by_subclass_ids)
                )
                and (
                    filter_by_schools is None
                    or any(s == s.school for c in filter_by_schools)
                )
                and (
                    filter_by_damage_types is None
                    or any(s == s.damage_type for c in filter_by_damage_types)
                )
                and (
                    filter_by_durations is None
                    or any(s == s.duration for c in filter_by_durations)
                )
                and (
                    filter_by_casting_times is None
                    or any(s == s.casting_time for c in filter_by_casting_times)
                )
                and (
                    filter_by_verbal_component is None
                    or s.components.verbal == filter_by_verbal_component
                )
                and (
                    filter_by_symbolic_component is None
                    or s.components.symbolic == filter_by_symbolic_component
                )
                and (
                    filter_by_material_component is None
                    or s.components.material == filter_by_material_component
                )
                and (
                    filter_by_concentration is None
                    or s.concentration == filter_by_concentration
                )
                and (filter_by_ritual is None or s.ritual == filter_by_ritual)
                and (
                    filter_by_source_ids is None
                    or any(source == s.source_id for source in filter_by_source_ids)
                )
            ):
                result.append(s)
        return result

    async def create(self, spell: AppSpell) -> None:
        self._store[spell.spell_id] = spell

    async def update(self, spell: AppSpell) -> None:
        self._store[spell.spell_id] = spell

    async def delete(self, spell_id: UUID) -> None:
        del self._store[spell_id]
