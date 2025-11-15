from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.weapon_kind import (
    CreateWeaponKindCommand,
    DeleteWeaponKindCommand,
    UpdateWeaponKindCommand,
)
from application.dto.query.weapon_kind import WeaponKindQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    WeaponKindUseCases,
    di_weapon_kind_use_cases,
)
from ports.http.web.v1.schemas.weapon_kind import (
    CreateWeaponKindDTO,
    CreateWeaponKindSchema,
    ReadWeaponKindSchema,
    UpdateWeaponKindDTO,
    UpdateWeaponKindSchema,
)


class WeaponKindController(Controller):
    path = "/weapon-kinds"
    tags = ["weapon kind"]

    dependencies = {"use_cases": Provide(di_weapon_kind_use_cases, sync_to_thread=True)}

    @get("/{weapon_kind_id:uuid}")
    async def get_weapon_kind(
        self, weapon_kind_id: UUID, use_cases: WeaponKindUseCases
    ) -> ReadWeaponKindSchema:
        weapon_kind = await use_cases.get_one.execute(
            WeaponKindQuery(weapon_kind_id=weapon_kind_id)
        )
        return ReadWeaponKindSchema.from_domain(weapon_kind)

    @get()
    async def get_weapon_kinds(
        self, use_cases: WeaponKindUseCases
    ) -> list[ReadWeaponKindSchema]:
        weapon_kinds = await use_cases.get_all.execute()
        return [
            ReadWeaponKindSchema.from_domain(weapon_kind)
            for weapon_kind in weapon_kinds
        ]

    @post(dto=CreateWeaponKindDTO)
    async def create_weapon_kind(
        self, weapon_kind: CreateWeaponKindSchema, use_cases: WeaponKindUseCases
    ) -> UUID:
        command = CreateWeaponKindCommand(user_id=uuid4(), **asdict(weapon_kind))
        return await use_cases.create.execute(command)

    @put("/{weapon_kind_id:uuid}", dto=UpdateWeaponKindDTO)
    async def update_weapon_kind(
        self,
        weapon_kind_id: UUID,
        weapon_kind: UpdateWeaponKindSchema,
        use_cases: WeaponKindUseCases,
    ) -> None:
        command = UpdateWeaponKindCommand(
            weapon_kind_id=weapon_kind_id, **asdict(weapon_kind)
        )
        await use_cases.update.execute(command)

    @delete("/{weapon_kind_id:uuid}")
    async def delete_weapon_kind(
        self, weapon_kind_id: UUID, use_cases: WeaponKindUseCases
    ) -> None:
        command = DeleteWeaponKindCommand(
            user_id=uuid4(), weapon_kind_id=weapon_kind_id
        )
        await use_cases.delete.execute(command)
