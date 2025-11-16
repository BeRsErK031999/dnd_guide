from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.subrace import (
    CreateSubraceCommand,
    DeleteSubraceCommand,
    UpdateSubraceCommand,
)
from application.dto.query.subrace import SubraceQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    SubraceUseCases,
    di_subrace_use_cases,
)
from ports.http.web.v1.schemas.subrace import (
    CreateSubraceSchema,
    ReadSubraceSchema,
    UpdateSubraceSchema,
)


class SubraceController(Controller):
    path = "/subraces"
    tags = ["subrace"]

    dependencies = {"use_cases": Provide(di_subrace_use_cases, sync_to_thread=True)}

    @get("/{subrace_id:uuid}")
    async def get_subrace(
        self, subrace_id: UUID, use_cases: SubraceUseCases
    ) -> ReadSubraceSchema:
        subrace = await use_cases.get_one.execute(SubraceQuery(subrace_id=subrace_id))
        return ReadSubraceSchema.from_domain(subrace)

    @get()
    async def get_subraces(self, use_cases: SubraceUseCases) -> list[ReadSubraceSchema]:
        subraces = await use_cases.get_all.execute()
        return [ReadSubraceSchema.from_domain(subrace) for subrace in subraces]

    @post()
    async def create_subrace(
        self, data: CreateSubraceSchema, use_cases: SubraceUseCases
    ) -> UUID:
        command = CreateSubraceCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{subrace_id:uuid}")
    async def update_subrace(
        self,
        subrace_id: UUID,
        data: UpdateSubraceSchema,
        use_cases: SubraceUseCases,
    ) -> None:
        subrace = UpdateSubraceCommand(
            user_id=uuid4(), subrace_id=subrace_id, **asdict(data)
        )
        await use_cases.update.execute(subrace)

    @delete("/{subrace_id:uuid}")
    async def delete_subrace(
        self, subrace_id: UUID, use_cases: SubraceUseCases
    ) -> None:
        command = DeleteSubraceCommand(user_id=uuid4(), subrace_id=subrace_id)
        await use_cases.delete.execute(command)
