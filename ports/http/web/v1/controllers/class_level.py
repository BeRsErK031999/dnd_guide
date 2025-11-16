from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.class_level import (
    CreateClassLevelCommand,
    DeleteClassLevelCommand,
    UpdateClassLevelCommand,
)
from application.dto.query.class_level import ClassLevelQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    ClassLevelUseCases,
    di_class_level_use_cases,
)
from ports.http.web.v1.schemas.class_level import (
    CreateClassLevelSchema,
    ReadClassLevelSchema,
    UpdateClassLevelSchema,
)


class ClassLevelController(Controller):
    path = "/class-levels"
    tags = ["class level"]

    dependencies = {"use_cases": Provide(di_class_level_use_cases, sync_to_thread=True)}

    @get("/{class_level_id:uuid}")
    async def get_class_level(
        self, class_level_id: UUID, use_cases: ClassLevelUseCases
    ) -> ReadClassLevelSchema:
        level = await use_cases.get_one.execute(
            ClassLevelQuery(class_level_id=class_level_id)
        )
        return ReadClassLevelSchema.from_domain(level)

    @get()
    async def get_class_levels(
        self, use_cases: ClassLevelUseCases
    ) -> list[ReadClassLevelSchema]:
        levels = await use_cases.get_all.execute()
        return [ReadClassLevelSchema.from_domain(level) for level in levels]

    @post()
    async def create_class_level(
        self, data: CreateClassLevelSchema, use_cases: ClassLevelUseCases
    ) -> UUID:
        command = CreateClassLevelCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{class_level_id:uuid}")
    async def update_class_level(
        self,
        class_level_id: UUID,
        data: UpdateClassLevelSchema,
        use_cases: ClassLevelUseCases,
    ) -> None:
        command = UpdateClassLevelCommand(class_level_id=class_level_id, **asdict(data))
        await use_cases.update.execute(command)

    @delete("/{class_level_id:uuid}")
    async def delete_class_level(
        self, class_level_id: UUID, use_cases: ClassLevelUseCases
    ) -> None:
        command = DeleteClassLevelCommand(
            user_id=uuid4(), class_level_id=class_level_id
        )
        await use_cases.delete.execute(command)
