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
    CreateClassLevelDTO,
    CreateClassLevelSchema,
    ReadClassLevelSchema,
    UpdateClassLevelDTO,
    UpdateClassLevelSchema,
)


class ClassLevelController(Controller):
    path = "/class-levels"
    tags = ["class levels"]

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

    @post(dto=CreateClassLevelDTO)
    async def create_class_level(
        self, class_level: CreateClassLevelSchema, use_cases: ClassLevelUseCases
    ) -> UUID:
        command = CreateClassLevelCommand(user_id=uuid4(), **asdict(class_level))
        return await use_cases.create.execute(command)

    @put("/{class_level_id:uuid}", dto=UpdateClassLevelDTO)
    async def update_class_level(
        self,
        class_level_id: UUID,
        class_level: UpdateClassLevelSchema,
        use_cases: ClassLevelUseCases,
    ) -> None:
        command = UpdateClassLevelCommand(
            class_level_id=class_level_id, **asdict(class_level)
        )
        await use_cases.update.execute(command)

    @delete("/{class_level_id:uuid}")
    async def delete_class_level(
        self, class_level_id: UUID, use_cases: ClassLevelUseCases
    ) -> None:
        command = DeleteClassLevelCommand(
            user_id=uuid4(), class_level_id=class_level_id
        )
        await use_cases.delete.execute(command)
