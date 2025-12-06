from uuid import UUID, uuid4

from application.dto.command.character_class import DeleteClassCommand
from application.dto.query.character_class import ClassesQuery, ClassQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import ClassUseCases, di_class_use_cases
from ports.http.web.v1.schemas.character_class import (
    CreateClassSchema,
    ReadClassSchema,
    UpdateClassSchema,
)


class ClassController(Controller):
    path = "/classes"
    tags = ["character class"]

    dependencies = {"use_cases": Provide(di_class_use_cases, sync_to_thread=True)}

    @get("/{class_id:uuid}")
    async def get_class(
        self, class_id: UUID, use_cases: ClassUseCases
    ) -> ReadClassSchema:
        character_class = await use_cases.get_one.execute(ClassQuery(class_id=class_id))
        return ReadClassSchema.from_app(character_class)

    @get()
    async def get_classes(
        self, search_by_name: str | None, use_cases: ClassUseCases
    ) -> list[ReadClassSchema]:
        query = ClassesQuery(search_by_name=search_by_name)
        classes = await use_cases.get_all.execute(query)
        return [
            ReadClassSchema.from_app(character_class) for character_class in classes
        ]

    @post()
    async def create_class(
        self, data: CreateClassSchema, use_cases: ClassUseCases
    ) -> UUID:
        return await use_cases.create.execute(data.to_command(uuid4()))

    @put("/{class_id:uuid}")
    async def update_class(
        self,
        class_id: UUID,
        data: UpdateClassSchema,
        use_cases: ClassUseCases,
    ) -> None:
        await use_cases.update.execute(data.to_command(uuid4(), class_id))

    @delete("/{class_id:uuid}")
    async def delete_class(self, class_id: UUID, use_cases: ClassUseCases) -> None:
        command = DeleteClassCommand(user_id=uuid4(), class_id=class_id)
        await use_cases.delete.execute(command)
