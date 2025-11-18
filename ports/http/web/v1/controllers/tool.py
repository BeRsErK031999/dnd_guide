from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.tool import (
    CreateToolCommand,
    DeleteToolCommand,
    UpdateToolCommand,
)
from application.dto.query.tool import ToolQuery, ToolsQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import ToolUseCases, di_tool_use_cases
from ports.http.web.v1.schemas.tool import (
    CreateToolSchema,
    ReadToolSchema,
    ReadToolTypeSchema,
    UpdateToolSchema,
)


class ToolController(Controller):
    path = "/tools"
    tags = ["tool"]

    dependencies = {"use_cases": Provide(di_tool_use_cases, sync_to_thread=True)}

    @get("/{tool_id:uuid}")
    async def get_tool(self, tool_id: UUID, use_cases: ToolUseCases) -> ReadToolSchema:
        tool = await use_cases.get_one.execute(ToolQuery(tool_id=tool_id))
        return ReadToolSchema.from_domain(tool)

    @get()
    async def get_tools(
        self, search_by_name: str | None, use_cases: ToolUseCases
    ) -> list[ReadToolSchema]:
        query = ToolsQuery(search_by_name=search_by_name)
        tools = await use_cases.get_all.execute(query)
        return [ReadToolSchema.from_domain(tool) for tool in tools]

    @post()
    async def create_tool(
        self, data: CreateToolSchema, use_cases: ToolUseCases
    ) -> UUID:
        command = CreateToolCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{tool_id:uuid}")
    async def update_tool(
        self,
        tool_id: UUID,
        data: UpdateToolSchema,
        use_cases: ToolUseCases,
    ) -> None:
        command = UpdateToolCommand(user_id=uuid4(), tool_id=tool_id, **asdict(data))
        await use_cases.update.execute(command)

    @delete("/{tool_id:uuid}")
    async def delete_tool(self, tool_id: UUID, use_cases: ToolUseCases) -> None:
        command = DeleteToolCommand(user_id=uuid4(), tool_id=tool_id)
        await use_cases.delete.execute(command)

    @get("/types")
    async def get_tool_types(self) -> ReadToolTypeSchema:
        return ReadToolTypeSchema.from_domain()
