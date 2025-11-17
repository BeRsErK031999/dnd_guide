from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.material_component import (
    CreateMaterialComponentCommand,
    DeleteMaterialComponentCommand,
    UpdateMaterialComponentCommand,
)
from application.dto.query.material_component import (
    MaterialComponentQuery,
    MaterialComponentsQuery,
)
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    MaterialComponentUseCases,
    di_material_component_use_cases,
)
from ports.http.web.v1.schemas.material_component import (
    CreateMaterialComponentSchema,
    ReadMaterialComponentSchema,
    UpdateMaterialComponentSchema,
)


class MaterialComponentController(Controller):
    path = "/material-components"
    tags = ["material component"]

    dependencies = {
        "use_cases": Provide(di_material_component_use_cases, sync_to_thread=True)
    }

    @get("/{material_id:uuid}")
    async def get_material(
        self, material_id: UUID, use_cases: MaterialComponentUseCases
    ) -> ReadMaterialComponentSchema:
        feature = await use_cases.get_one.execute(
            MaterialComponentQuery(material_id=material_id)
        )
        return ReadMaterialComponentSchema.from_domain(feature)

    @get()
    async def get_materials(
        self, search_by_name: str | None, use_cases: MaterialComponentUseCases
    ) -> list[ReadMaterialComponentSchema]:
        query = MaterialComponentsQuery(search_by_name=search_by_name)
        materials = await use_cases.get_all.execute(query)
        return [
            ReadMaterialComponentSchema.from_domain(material) for material in materials
        ]

    @post()
    async def create_material(
        self,
        data: CreateMaterialComponentSchema,
        use_cases: MaterialComponentUseCases,
    ) -> UUID:
        command = CreateMaterialComponentCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{material_id:uuid}")
    async def update_material(
        self,
        material_id: UUID,
        data: UpdateMaterialComponentSchema,
        use_cases: MaterialComponentUseCases,
    ) -> None:
        command = UpdateMaterialComponentCommand(
            user_id=uuid4(), material_id=material_id, **asdict(data)
        )
        await use_cases.update.execute(command)

    @delete("/{material_id:uuid}")
    async def delete_material(
        self, material_id: UUID, use_cases: MaterialComponentUseCases
    ) -> None:
        command = DeleteMaterialComponentCommand(
            user_id=uuid4(), material_id=material_id
        )
        await use_cases.delete.execute(command)
