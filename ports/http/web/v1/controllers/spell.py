from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.spell import (
    CreateSpellCommand,
    DeleteSpellCommand,
    UpdateSpellCommand,
)
from application.dto.query.spell import SpellQuery, SpellsQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import SpellUseCases, di_spell_use_cases
from ports.http.web.v1.schemas.spell import (
    CreateSpellSchema,
    ReadSpellSchema,
    ReadSpellSchoolSchema,
    UpdateSpellSchema,
)


class SpellController(Controller):
    path = "/spells"
    tags = ["spell"]

    dependencies = {"use_cases": Provide(di_spell_use_cases, sync_to_thread=True)}

    @get("/{spell_id:uuid}")
    async def get_spell(
        self, spell_id: UUID, use_cases: SpellUseCases
    ) -> ReadSpellSchema:
        spell = await use_cases.get_one.execute(SpellQuery(spell_id=spell_id))
        return ReadSpellSchema.from_domain(spell)

    @get()
    async def get_spells(
        self,
        search_by_name: str | None,
        filter_by_class_ids: list[UUID] | None,
        filter_by_subclass_ids: list[UUID] | None,
        filter_by_schools: list[str] | None,
        filter_by_damage_types: list[str] | None,
        filter_by_durations: list[str] | None,
        filter_by_casting_times: list[str] | None,
        filter_by_verbal_component: bool | None,
        filter_by_symbolic_component: bool | None,
        filter_by_material_component: bool | None,
        filter_by_concentration: bool | None,
        filter_by_ritual: bool | None,
        filter_by_source_ids: list[UUID] | None,
        use_cases: SpellUseCases,
    ) -> list[ReadSpellSchema]:
        query = SpellsQuery(
            search_by_name=search_by_name,
            filter_by_class_ids=filter_by_class_ids,
            filter_by_subclass_ids=filter_by_subclass_ids,
            filter_by_schools=filter_by_schools,
            filter_by_damage_types=filter_by_damage_types,
            filter_by_durations=filter_by_durations,
            filter_by_casting_times=filter_by_casting_times,
            filter_by_verbal_component=filter_by_verbal_component,
            filter_by_symbolic_component=filter_by_symbolic_component,
            filter_by_material_component=filter_by_material_component,
            filter_by_concentration=filter_by_concentration,
            filter_by_ritual=filter_by_ritual,
            filter_by_source_ids=filter_by_source_ids,
        )
        spells = await use_cases.get_all.execute(query)
        return [ReadSpellSchema.from_domain(spell) for spell in spells]

    @post()
    async def create_spell(
        self, data: CreateSpellSchema, use_cases: SpellUseCases
    ) -> UUID:
        command = CreateSpellCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{spell_id:uuid}")
    async def update_spell(
        self,
        spell_id: UUID,
        data: UpdateSpellSchema,
        use_cases: SpellUseCases,
    ) -> None:
        command = UpdateSpellCommand(user_id=uuid4(), spell_id=spell_id, **asdict(data))
        await use_cases.update.execute(command)

    @delete("/{spell_id:uuid}")
    async def delete_spell(self, spell_id: UUID, use_cases: SpellUseCases) -> None:
        command = DeleteSpellCommand(user_id=uuid4(), spell_id=spell_id)
        await use_cases.delete.execute(command)

    @get("/schools")
    async def get_schools(self) -> ReadSpellSchoolSchema:
        return ReadSpellSchoolSchema.from_domain()
