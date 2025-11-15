from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.armor import (
    CreateArmorCommand,
    DeleteArmorCommand,
    UpdateArmorCommand,
)
from application.dto.query.armor import ArmorQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.providers import UseCases, di_use_cases
from ports.http.web.schemas.armor import (
    CreateArmorDTO,
    CreateArmorSchema,
    ReadArmorSchema,
    UpdateArmorDTO,
    UpdateArmorSchema,
)


class ArmorController(Controller):
    path = "/armors"
    tags = ["armor"]

    dependencies = {"use_cases": Provide(di_use_cases, sync_to_thread=True)}

    @get("/{armor_id:uuid}")
    async def get_armor(self, armor_id: UUID, use_cases: UseCases) -> ReadArmorSchema:
        armor = await use_cases.get_armor.execute(ArmorQuery(armor_id=armor_id))
        return ReadArmorSchema.from_domain(armor)

    @get()
    async def get_armors(self, use_cases: UseCases) -> list[ReadArmorSchema]:
        armors = await use_cases.get_armors.execute()
        return [ReadArmorSchema.from_domain(armor) for armor in armors]

    @post(dto=CreateArmorDTO)
    async def create_armor(self, armor: CreateArmorSchema, use_cases: UseCases) -> UUID:
        command = CreateArmorCommand(user_id=uuid4(), **asdict(armor))
        return await use_cases.create_armor.execute(command)

    @put("/{armor_id:uuid}", dto=UpdateArmorDTO)
    async def update_armor(
        self, armor_id: UUID, armor: UpdateArmorSchema, use_cases: UseCases
    ) -> None:
        command = UpdateArmorCommand(armor_id=armor_id, **asdict(armor))
        await use_cases.update_armor.execute(command)

    @delete("/{armor_id:uuid}")
    async def delete_armor(self, armor_id: UUID, use_cases: UseCases) -> None:
        command = DeleteArmorCommand(user_id=uuid4(), armor_id=armor_id)
        await use_cases.delete_armor.execute(command)
