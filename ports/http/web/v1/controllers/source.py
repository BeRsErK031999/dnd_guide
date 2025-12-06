from uuid import UUID, uuid4

from application.dto.command.source import DeleteSourceCommand
from application.dto.query.source import SourceQuery, SourcesQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import SourceUseCases, di_source_use_cases
from ports.http.web.v1.schemas.source import (
    CreateSourceSchema,
    ReadSourceSchema,
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
        return ReadSourceSchema.from_app(source)

    @get()
    async def get_sources(
        self, search_by_name: str | None, use_cases: SourceUseCases
    ) -> list[ReadSourceSchema]:
        query = SourcesQuery(search_by_name=search_by_name)
        sources = await use_cases.get_all.execute(query)
        return [ReadSourceSchema.from_app(source) for source in sources]

    @post()
    async def create_source(
        self, data: CreateSourceSchema, use_cases: SourceUseCases
    ) -> UUID:
        return await use_cases.create.execute(data.to_command(uuid4()))

    @put("/{source_id:uuid}")
    async def update_source(
        self,
        source_id: UUID,
        data: UpdateSourceSchema,
        use_cases: SourceUseCases,
    ) -> None:
        await use_cases.update.execute(data.to_command(uuid4(), source_id))

    @delete("/{source_id:uuid}")
    async def delete_source(self, source_id: UUID, use_cases: SourceUseCases) -> None:
        command = DeleteSourceCommand(user_id=uuid4(), source_id=source_id)
        await use_cases.delete.execute(command)
