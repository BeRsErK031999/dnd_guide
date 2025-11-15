from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.character_class import (
    CreateClassCommand,
    DeleteClassCommand,
    UpdateClassCommand,
)
from application.dto.query.character_class import ClassQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import ClassUseCases, di_class_use_cases
from ports.http.web.v1.schemas.character_class import (
    CreateClassDTO,
    CreateClassSchema,
    ReadClassSchema,
    UpdateClassDTO,
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
        armor = await use_cases.get_one.execute(ClassQuery(class_id=class_id))
        return ReadClassSchema.from_domain(armor)

    @get()
    async def get_classes(self, use_cases: ClassUseCases) -> list[ReadClassSchema]:
        armors = await use_cases.get_all.execute()
        return [ReadClassSchema.from_domain(armor) for armor in armors]

    @post(dto=CreateClassDTO)
    async def create_class(
        self, armor: CreateClassSchema, use_cases: ClassUseCases
    ) -> UUID:
        command = CreateClassCommand(user_id=uuid4(), **asdict(armor))
        return await use_cases.create.execute(command)

    @put("/{class_id:uuid}", dto=UpdateClassDTO)
    async def update_class(
        self, class_id: UUID, armor: UpdateClassSchema, use_cases: ClassUseCases
    ) -> None:
        command = UpdateClassCommand(class_id=class_id, **asdict(armor))
        await use_cases.update.execute(command)

    @delete("/{class_id:uuid}")
    async def delete_class(self, class_id: UUID, use_cases: ClassUseCases) -> None:
        command = DeleteClassCommand(user_id=uuid4(), class_id=class_id)
        await use_cases.delete.execute(command)
