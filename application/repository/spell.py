from abc import ABC, abstractmethod
from uuid import UUID

from domain.spell import Spell


class SpellRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, spell_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, spell_id: UUID) -> Spell:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Spell]:
        raise NotImplemented

    @abstractmethod
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
    ) -> list[Spell]:
        raise NotImplemented

    @abstractmethod
    async def create(self, spell: Spell) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, spell: Spell) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, spell_id: UUID) -> None:
        raise NotImplemented
