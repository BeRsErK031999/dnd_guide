from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.spell import AppSpell


class SpellRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, spell_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, spell_id: UUID) -> AppSpell:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppSpell]:
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
        filter_by_material_ids: list[UUID] | None = None,
        filter_by_concentration: bool | None = None,
        filter_by_ritual: bool | None = None,
        filter_by_source_ids: list[UUID] | None = None,
    ) -> list[AppSpell]:
        raise NotImplemented

    @abstractmethod
    async def save(self, spell: AppSpell) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, spell_id: UUID) -> None:
        raise NotImplemented
