from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.spell import (
    CreateSpellCommand,
    DeleteSpellCommand,
    UpdateSpellCommand,
)
from application.dto.query.spell import SpellQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import SpellUseCases, di_spell_use_cases
from ports.http.web.v1.schemas.spell import (
    CreateSpellDTO,
    CreateSpellSchema,
    ReadSpellSchema,
    UpdateSpellDTO,
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
    async def get_spells(self, use_cases: SpellUseCases) -> list[ReadSpellSchema]:
        spells = await use_cases.get_all.execute()
        return [ReadSpellSchema.from_domain(spell) for spell in spells]

    @post(dto=CreateSpellDTO)
    async def create_spell(
        self, spell: CreateSpellSchema, use_cases: SpellUseCases
    ) -> UUID:
        command = CreateSpellCommand(user_id=uuid4(), **asdict(spell))
        return await use_cases.create.execute(command)

    @put("/{spell_id:uuid}", dto=UpdateSpellDTO)
    async def update_spell(
        self,
        spell_id: UUID,
        spell: UpdateSpellSchema,
        use_cases: SpellUseCases,
    ) -> None:
        command = UpdateSpellCommand(spell_id=spell_id, **asdict(spell))
        await use_cases.update.execute(command)

    @delete("/{spell_id:uuid}")
    async def delete_spell(self, spell_id: UUID, use_cases: SpellUseCases) -> None:
        command = DeleteSpellCommand(user_id=uuid4(), spell_id=spell_id)
        await use_cases.delete.execute(command)
