from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.creature_size import (
    CreateCreatureSizeCommand,
    DeleteCreatureSizeCommand,
    UpdateCreatureSizeCommand,
)
from application.dto.query.creature_size import CreatureSizeQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    CreatureSizeUseCases,
    di_creature_size_use_cases,
)
from ports.http.web.v1.schemas.creature_size import (
    CreateCreatureSizeSchema,
    ReadCreatureSizeSchema,
    UpdateCreatureSizeSchema,
)


class CreatureSizeController(Controller):
    path = "/creature-sizes"
    tags = ["creature size"]

    dependencies = {
        "use_cases": Provide(di_creature_size_use_cases, sync_to_thread=True)
    }

    @get("/{size_id:uuid}")
    async def get_size(
        self, size_id: UUID, use_cases: CreatureSizeUseCases
    ) -> ReadCreatureSizeSchema:
        creature_size = await use_cases.get_one.execute(
            CreatureSizeQuery(size_id=size_id)
        )
        return ReadCreatureSizeSchema.from_domain(creature_size)

    @get()
    async def get_sizes(
        self, use_cases: CreatureSizeUseCases
    ) -> list[ReadCreatureSizeSchema]:
        creature_sizes = await use_cases.get_all.execute()
        return [
            ReadCreatureSizeSchema.from_domain(creature_size)
            for creature_size in creature_sizes
        ]

    @post()
    async def create_size(
        self, data: CreateCreatureSizeSchema, use_cases: CreatureSizeUseCases
    ) -> UUID:
        command = CreateCreatureSizeCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{size_id:uuid}")
    async def update_size(
        self,
        size_id: UUID,
        data: UpdateCreatureSizeSchema,
        use_cases: CreatureSizeUseCases,
    ) -> None:
        command = UpdateCreatureSizeCommand(size_id=size_id, **asdict(data))
        await use_cases.update.execute(command)

    @delete("/{size_id:uuid}")
    async def delete_size(self, size_id: UUID, use_cases: CreatureSizeUseCases) -> None:
        command = DeleteCreatureSizeCommand(user_id=uuid4(), size_id=size_id)
        await use_cases.delete.execute(command)
