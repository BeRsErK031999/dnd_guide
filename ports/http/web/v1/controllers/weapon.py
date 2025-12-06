from uuid import UUID, uuid4

from application.dto.command.weapon import DeleteWeaponCommand
from application.dto.query.weapon import WeaponQuery, WeaponsQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import WeaponUseCases, di_weapon_use_cases
from ports.http.web.v1.schemas.weapon import (
    CreateWeaponSchema,
    ReadWeaponSchema,
    UpdateWeaponSchema,
)
from ports.http.web.v1.schemas.weapon_kind import ReadWeaponTypeSchema


class WeaponController(Controller):
    path = "/weapons"
    tags = ["weapon"]

    dependencies = {"use_cases": Provide(di_weapon_use_cases, sync_to_thread=True)}

    @get("/{weapon_id:uuid}")
    async def get_weapon(
        self, weapon_id: UUID, use_cases: WeaponUseCases
    ) -> ReadWeaponSchema:
        weapon = await use_cases.get_one.execute(WeaponQuery(weapon_id=weapon_id))
        return ReadWeaponSchema.from_app(weapon)

    @get()
    async def get_weapons(
        self,
        search_by_name: str | None,
        filter_by_kind_ids: list[UUID] | None,
        filter_by_damage_types: list[str] | None,
        filter_by_property_ids: list[UUID] | None,
        filter_by_material_ids: list[UUID] | None,
        use_cases: WeaponUseCases,
    ) -> list[ReadWeaponSchema]:
        query = WeaponsQuery(
            search_by_name=search_by_name,
            filter_by_kind_ids=filter_by_kind_ids,
            filter_by_damage_types=filter_by_damage_types,
            filter_by_property_ids=filter_by_property_ids,
            filter_by_material_ids=filter_by_material_ids,
        )
        weapons = await use_cases.get_all.execute(query)
        return [ReadWeaponSchema.from_app(weapon) for weapon in weapons]

    @post()
    async def create_weapon(
        self, data: CreateWeaponSchema, use_cases: WeaponUseCases
    ) -> UUID:
        return await use_cases.create.execute(data.to_command(uuid4()))

    @put("/{weapon_id:uuid}")
    async def update_weapon(
        self,
        weapon_id: UUID,
        data: UpdateWeaponSchema,
        use_cases: WeaponUseCases,
    ) -> None:
        await use_cases.update.execute(data.to_command(uuid4(), weapon_id))

    @delete("/{weapon_id:uuid}")
    async def delete_weapon(self, weapon_id: UUID, use_cases: WeaponUseCases) -> None:
        command = DeleteWeaponCommand(user_id=uuid4(), weapon_id=weapon_id)
        await use_cases.delete.execute(command)

    @get("/types")
    async def get_weapon_types(self) -> ReadWeaponTypeSchema:
        return ReadWeaponTypeSchema.from_domain()
