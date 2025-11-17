from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.armor import (
    CreateArmorCommand,
    DeleteArmorCommand,
    UpdateArmorCommand,
)
from application.dto.query.armor import ArmorQuery, ArmorsQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import ArmorUseCases, di_armor_use_cases
from ports.http.web.v1.schemas.armor import (
    CreateArmorSchema,
    ReadArmorSchema,
    ReadArmorTypeSchema,
    UpdateArmorSchema,
)


class ArmorController(Controller):
    path = "/armors"
    tags = ["armor"]

    dependencies = {"use_cases": Provide(di_armor_use_cases, sync_to_thread=True)}

    @get("/{armor_id:uuid}")
    async def get_armor(
        self, armor_id: UUID, use_cases: ArmorUseCases
    ) -> ReadArmorSchema:
        armor = await use_cases.get_one.execute(ArmorQuery(armor_id=armor_id))
        return ReadArmorSchema.from_domain(armor)

    @get()
    async def get_armors(
        self,
        search_by_name: str | None,
        filter_by_armor_types: list[str] | None,
        filter_by_material_ids: list[UUID] | None,
        use_cases: ArmorUseCases,
    ) -> list[ReadArmorSchema]:
        query = ArmorsQuery(
            search_by_name=search_by_name,
            filter_by_armor_types=filter_by_armor_types,
            filter_by_material_ids=filter_by_material_ids,
        )
        armors = await use_cases.get_all.execute(query)
        return [ReadArmorSchema.from_domain(armor) for armor in armors]

    @post()
    async def create_armor(
        self, data: CreateArmorSchema, use_cases: ArmorUseCases
    ) -> UUID:
        command = CreateArmorCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{armor_id:uuid}")
    async def update_armor(
        self, armor_id: UUID, data: UpdateArmorSchema, use_cases: ArmorUseCases
    ) -> None:
        command = UpdateArmorCommand(user_id=uuid4(), armor_id=armor_id, **asdict(data))
        await use_cases.update.execute(command)

    @delete("/{armor_id:uuid}")
    async def delete_armor(self, armor_id: UUID, use_cases: ArmorUseCases) -> None:
        command = DeleteArmorCommand(user_id=uuid4(), armor_id=armor_id)
        await use_cases.delete.execute(command)

    @get("/types")
    async def get_armor_types(self) -> ReadArmorTypeSchema:
        return ReadArmorTypeSchema.from_domain()
