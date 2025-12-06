from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.material import (
    CreateMaterialCommand,
    DeleteMaterialCommand,
    UpdateMaterialCommand,
)
from application.dto.query.material import MaterialQuery, MaterialsQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    MaterialUseCases,
    di_material_use_cases,
)
from ports.http.web.v1.schemas.material import (
    CreateMaterialSchema,
    ReadMaterialSchema,
    UpdateMaterialSchema,
)


class MaterialController(Controller):
    path = "/materials"
    tags = ["material"]

    dependencies = {"use_cases": Provide(di_material_use_cases, sync_to_thread=True)}

    @get("/{material_id:uuid}")
    async def get_material(
        self, material_id: UUID, use_cases: MaterialUseCases
    ) -> ReadMaterialSchema:
        material = await use_cases.get_one.execute(
            MaterialQuery(material_id=material_id)
        )
        return ReadMaterialSchema.from_app(material)

    @get()
    async def get_materials(
        self, search_by_name: str | None, use_cases: MaterialUseCases
    ) -> list[ReadMaterialSchema]:
        query = MaterialsQuery(search_by_name=search_by_name)
        materials = await use_cases.get_all.execute(query)
        return [ReadMaterialSchema.from_app(material) for material in materials]

    @post()
    async def create_material(
        self, data: CreateMaterialSchema, use_cases: MaterialUseCases
    ) -> UUID:
        command = CreateMaterialCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{material_id:uuid}")
    async def update_material(
        self,
        material_id: UUID,
        data: UpdateMaterialSchema,
        use_cases: MaterialUseCases,
    ) -> None:
        command = UpdateMaterialCommand(
            user_id=uuid4(), material_id=material_id, **asdict(data)
        )
        await use_cases.update.execute(command)

    @delete("/{material_id:uuid}")
    async def delete_material(
        self, material_id: UUID, use_cases: MaterialUseCases
    ) -> None:
        command = DeleteMaterialCommand(user_id=uuid4(), material_id=material_id)
        await use_cases.delete.execute(command)
