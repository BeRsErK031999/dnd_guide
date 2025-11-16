from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.creature_type import (
    CreateCreatureTypeCommand,
    DeleteCreatureTypeCommand,
    UpdateCreatureTypeCommand,
)
from application.dto.query.creature_type import CreatureTypeQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    CreatureTypeUseCases,
    di_creature_type_use_cases,
)
from ports.http.web.v1.schemas.creature_type import (
    CreateCreatureTypeSchema,
    ReadCreatureTypeSchema,
    UpdateCreatureTypeSchema,
)


class CreatureTypeController(Controller):
    path = "/creature-types"
    tags = ["creature type"]

    dependencies = {
        "use_cases": Provide(di_creature_type_use_cases, sync_to_thread=True)
    }

    @get("/{type_id:uuid}")
    async def get_type(
        self, type_id: UUID, use_cases: CreatureTypeUseCases
    ) -> ReadCreatureTypeSchema:
        creature_type = await use_cases.get_one.execute(
            CreatureTypeQuery(type_id=type_id)
        )
        return ReadCreatureTypeSchema.from_domain(creature_type)

    @get()
    async def get_types(
        self, use_cases: CreatureTypeUseCases
    ) -> list[ReadCreatureTypeSchema]:
        creature_types = await use_cases.get_all.execute()
        return [
            ReadCreatureTypeSchema.from_domain(creature_type)
            for creature_type in creature_types
        ]

    @post()
    async def create_type(
        self, data: CreateCreatureTypeSchema, use_cases: CreatureTypeUseCases
    ) -> UUID:
        command = CreateCreatureTypeCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{type_id:uuid}")
    async def update_type(
        self,
        type_id: UUID,
        data: UpdateCreatureTypeSchema,
        use_cases: CreatureTypeUseCases,
    ) -> None:
        command = UpdateCreatureTypeCommand(type_id=type_id, **asdict(data))
        await use_cases.update.execute(command)

    @delete("/{type_id:uuid}")
    async def delete_type(self, type_id: UUID, use_cases: CreatureTypeUseCases) -> None:
        command = DeleteCreatureTypeCommand(user_id=uuid4(), type_id=type_id)
        await use_cases.delete.execute(command)
