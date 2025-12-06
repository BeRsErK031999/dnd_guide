from uuid import UUID, uuid4

from application.dto.command.class_level import DeleteClassLevelCommand
from application.dto.query.class_level import ClassLevelQuery, ClassLevelsQuery
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
        return ReadClassLevelSchema.from_app(level)

    @get()
    async def get_class_levels(
        self, filter_by_class_id: UUID, use_cases: ClassLevelUseCases
    ) -> list[ReadClassLevelSchema]:
        query = ClassLevelsQuery(filter_by_class_id=filter_by_class_id)
        levels = await use_cases.get_all.execute(query)
        return [ReadClassLevelSchema.from_app(level) for level in levels]

    @post()
    async def create_class_level(
        self, data: CreateClassLevelSchema, use_cases: ClassLevelUseCases
    ) -> UUID:
        return await use_cases.create.execute(data.to_command(uuid4()))

    @put("/{class_level_id:uuid}")
    async def update_class_level(
        self,
        class_level_id: UUID,
        data: UpdateClassLevelSchema,
        use_cases: ClassLevelUseCases,
    ) -> None:
        await use_cases.update.execute(data.to_command(uuid4(), class_level_id))

    @delete("/{class_level_id:uuid}")
    async def delete_class_level(
        self, class_level_id: UUID, use_cases: ClassLevelUseCases
    ) -> None:
        command = DeleteClassLevelCommand(
            user_id=uuid4(), class_level_id=class_level_id
        )
        await use_cases.delete.execute(command)
