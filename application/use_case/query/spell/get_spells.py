from application.dto.model.spell import AppSpell
from application.dto.query.spell import SpellsQuery
from application.repository import SpellRepository


class GetSpellsUseCase:
    def __init__(self, spell_repository: SpellRepository):
        self.__repository = spell_repository

    async def execute(self, query: SpellsQuery) -> list[AppSpell]:
        return await self.__repository.filter(
            search_by_name=query.search_by_name,
            filter_by_class_ids=query.filter_by_class_ids,
            filter_by_subclass_ids=query.filter_by_subclass_ids,
            filter_by_schools=query.filter_by_schools,
            filter_by_damage_types=query.filter_by_damage_types,
            filter_by_durations=query.filter_by_durations,
            filter_by_casting_times=query.filter_by_casting_times,
            filter_by_verbal_component=query.filter_by_verbal_component,
            filter_by_symbolic_component=query.filter_by_symbolic_component,
            filter_by_material_component=query.filter_by_material_component,
            filter_by_concentration=query.filter_by_concentration,
            filter_by_ritual=query.filter_by_ritual,
            filter_by_source_ids=query.filter_by_source_ids,
        )
