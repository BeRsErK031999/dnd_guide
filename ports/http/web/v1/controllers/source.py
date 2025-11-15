from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.source import (
    CreateSourceCommand,
    DeleteSourceCommand,
    UpdateSourceCommand,
)
from application.dto.query.source import SourceQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import SourceUseCases, di_source_use_cases
from ports.http.web.v1.schemas.source import (
    CreateSourceDTO,
    CreateSourceSchema,
    ReadSourceSchema,
    UpdateSourceDTO,
    UpdateSourceSchema,
)


class SourceController(Controller):
    path = "/sources"
    tags = ["source"]

    dependencies = {"use_cases": Provide(di_source_use_cases, sync_to_thread=True)}

    @get("/{source_id:uuid}")
    async def get_source(
        self, source_id: UUID, use_cases: SourceUseCases
    ) -> ReadSourceSchema:
        source = await use_cases.get_one.execute(SourceQuery(source_id=source_id))
        return ReadSourceSchema.from_domain(source)

    @get()
    async def get_sources(self, use_cases: SourceUseCases) -> list[ReadSourceSchema]:
        sources = await use_cases.get_all.execute()
        return [ReadSourceSchema.from_domain(source) for source in sources]

    @post(dto=CreateSourceDTO)
    async def create_source(
        self, source: CreateSourceSchema, use_cases: SourceUseCases
    ) -> UUID:
        command = CreateSourceCommand(user_id=uuid4(), **asdict(source))
        return await use_cases.create.execute(command)

    @put("/{source_id:uuid}", dto=UpdateSourceDTO)
    async def update_source(
        self,
        source_id: UUID,
        source: UpdateSourceSchema,
        use_cases: SourceUseCases,
    ) -> None:
        command = UpdateSourceCommand(source_id=source_id, **asdict(source))
        await use_cases.update.execute(command)

    @delete("/{source_id:uuid}")
    async def delete_source(self, source_id: UUID, use_cases: SourceUseCases) -> None:
        command = DeleteSourceCommand(user_id=uuid4(), source_id=source_id)
        await use_cases.delete.execute(command)
