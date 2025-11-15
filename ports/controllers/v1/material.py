from dataclasses import asdict
from re import S
from uuid import UUID, uuid4

from application.dto.command.material import (
    CreateMaterialCommand,
    DeleteMaterialCommand,
    UpdateMaterialCommand,
)
from application.dto.query.material import MaterialQuery
from domain.armor import Armor
from domain.material import Material
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.providers import Container, di_container
from ports.schemas.material import (
    CreateMaterialDTO,
    CreateMaterialSchema,
    ReadMaterialSchema,
    UpdateMaterialDTO,
    UpdateMaterialSchema,
)


class MaterialController(Controller):
    path = "/materials"
    tags = ["material"]

    dependencies = {"container": Provide(di_container, sync_to_thread=True)}

    @get("/{material_id:uuid}")
    async def get_material(
        self, material_id: UUID, container: Container
    ) -> ReadMaterialSchema:
        material = await container.use_cases.get_material.execute(
            MaterialQuery(material_id=material_id)
        )
        return ReadMaterialSchema.from_domain(material)

    @get()
    async def get_materials(self, container: Container) -> list[ReadMaterialSchema]:
        materials = await container.use_cases.get_materials.execute()
        return [ReadMaterialSchema.from_domain(material) for material in materials]

    @post(dto=CreateMaterialDTO)
    async def create_material(
        self, material: CreateMaterialSchema, container: Container
    ) -> UUID:
        command = CreateMaterialCommand(user_id=uuid4(), **asdict(material))
        return await container.use_cases.create_material.execute(command)

    @put("/{material_id:uuid}", dto=UpdateMaterialDTO)
    async def update_material(
        self, material_id: UUID, material: UpdateMaterialSchema, container: Container
    ) -> None:
        command = UpdateMaterialCommand(material_id=material_id, **asdict(material))
        await container.use_cases.update_material.execute(command)

    @delete("/{material_id:uuid}")
    async def delete_material(self, material_id: UUID, container: Container) -> None:
        command = DeleteMaterialCommand(user_id=uuid4(), material_id=material_id)
        await container.use_cases.delete_material.execute(command)
