from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.weapon_property import (
    CreateWeaponPropertyCommand,
    DeleteWeaponPropertyCommand,
    UpdateWeaponPropertyCommand,
)
from application.dto.query.weapon_property import (
    WeaponPropertiesQuery,
    WeaponPropertyQuery,
)
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    WeaponPropertyUseCases,
    di_weapon_property_use_cases,
)
from ports.http.web.v1.schemas.weapon_property import (
    CreateWeaponPropertySchema,
    ReadWeaponPropertyNameSchema,
    ReadWeaponPropertySchema,
    UpdateWeaponPropertySchema,
)


class WeaponPropertyController(Controller):
    path = "/weapon_properties"
    tags = ["weapon property"]

    dependencies = {
        "use_cases": Provide(di_weapon_property_use_cases, sync_to_thread=True)
    }

    @get("/{weapon_property_id:uuid}")
    async def get_weapon_property(
        self, weapon_property_id: UUID, use_cases: WeaponPropertyUseCases
    ) -> ReadWeaponPropertySchema:
        weapon_property = await use_cases.get_one.execute(
            WeaponPropertyQuery(weapon_property_id=weapon_property_id)
        )
        return ReadWeaponPropertySchema.from_domain(weapon_property)

    @get()
    async def get_weapon_properties(
        self, search_by_name: str | None, use_cases: WeaponPropertyUseCases
    ) -> list[ReadWeaponPropertySchema]:
        query = WeaponPropertiesQuery(search_by_name=search_by_name)
        weapon_properties = await use_cases.get_all.execute(query)
        return [
            ReadWeaponPropertySchema.from_domain(weapon_property)
            for weapon_property in weapon_properties
        ]

    @post()
    async def create_weapon_property(
        self,
        data: CreateWeaponPropertySchema,
        use_cases: WeaponPropertyUseCases,
    ) -> UUID:
        command = CreateWeaponPropertyCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{weapon_property_id:uuid}")
    async def update_weapon_property(
        self,
        weapon_property_id: UUID,
        data: UpdateWeaponPropertySchema,
        use_cases: WeaponPropertyUseCases,
    ) -> None:
        command = UpdateWeaponPropertyCommand(
            user_id=uuid4(), weapon_property_id=weapon_property_id, **asdict(data)
        )
        await use_cases.update.execute(command)

    @delete("/{weapon_property_id:uuid}")
    async def delete_weapon_property(
        self, weapon_property_id: UUID, use_cases: WeaponPropertyUseCases
    ) -> None:
        command = DeleteWeaponPropertyCommand(
            user_id=uuid4(), weapon_property_id=weapon_property_id
        )
        await use_cases.delete.execute(command)

    @get("/names")
    async def get_weapon_property_names(self) -> ReadWeaponPropertyNameSchema:
        return ReadWeaponPropertyNameSchema.from_domain()
