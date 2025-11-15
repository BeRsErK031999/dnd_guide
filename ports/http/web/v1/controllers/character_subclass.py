from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.character_subclass import (
    CreateSubclassCommand,
    DeleteSubclassCommand,
    UpdateSubclassCommand,
)
from application.dto.query.character_subclass import SubclassQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    SubclassUseCases,
    di_subclass_use_cases,
)
from ports.http.web.v1.schemas.character_subclass import (
    CreateSubclassDTO,
    CreateSubclassSchema,
    ReadSubclassSchema,
    UpdateSubclassDTO,
    UpdateSubclassSchema,
)


class SubclassController(Controller):
    path = "/subclasses"
    tags = ["character subclass"]

    dependencies = {"use_cases": Provide(di_subclass_use_cases, sync_to_thread=True)}

    @get("/{subclass_id:uuid}")
    async def get_subclass(
        self, subclass_id: UUID, use_cases: SubclassUseCases
    ) -> ReadSubclassSchema:
        subclass = await use_cases.get_one.execute(
            SubclassQuery(subclass_id=subclass_id)
        )
        return ReadSubclassSchema.from_domain(subclass)

    @get()
    async def get_subclasses(
        self, use_cases: SubclassUseCases
    ) -> list[ReadSubclassSchema]:
        subclasses = await use_cases.get_all.execute()
        return [ReadSubclassSchema.from_domain(subclass) for subclass in subclasses]

    @post(dto=CreateSubclassDTO)
    async def create_subclass(
        self, subclass: CreateSubclassSchema, use_cases: SubclassUseCases
    ) -> UUID:
        command = CreateSubclassCommand(user_id=uuid4(), **asdict(subclass))
        return await use_cases.create.execute(command)

    @put("/{subclass_id:uuid}", dto=UpdateSubclassDTO)
    async def update_subclass(
        self,
        subclass_id: UUID,
        subclass: UpdateSubclassSchema,
        use_cases: SubclassUseCases,
    ) -> None:
        command = UpdateSubclassCommand(subclass_id=subclass_id, **asdict(subclass))
        await use_cases.update.execute(command)

    @delete("/{subclass_id:uuid}")
    async def delete_subclass(
        self, subclass_id: UUID, use_cases: SubclassUseCases
    ) -> None:
        command = DeleteSubclassCommand(user_id=uuid4(), subclass_id=subclass_id)
        await use_cases.delete.execute(command)
