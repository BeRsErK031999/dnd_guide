from application.dto.command.material import DeleteMaterialCommand
from application.repository import (
    ArmorRepository,
    MaterialRepository,
    UserRepository,
    WeaponRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteMaterialUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        material_repository: MaterialRepository,
        armor_repository: ArmorRepository,
        weapon_repository: WeaponRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._material_repository = material_repository
        self._armor_repository = armor_repository
        self._weapon_repository = weapon_repository

    async def execute(self, command: DeleteMaterialCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._material_repository.id_exists(command.material_id):
            raise DomainError.not_found(
                f"материала с id {command.material_id} не существует"
            )
        exists_armors = await self._armor_repository.filter(
            filter_by_material_ids=[command.material_id]
        )
        if len(exists_armors) > 0:
            raise DomainError.invalid_data(
                "материал используется в доспехах: "
                f"{", ".join([a.name for a in exists_armors])}"
            )
        exists_weapons = await self._weapon_repository.filter(
            filter_by_material_ids=[command.material_id]
        )
        if len(exists_weapons) > 0:
            raise DomainError.invalid_data(
                "материал используется в оружии: "
                f"{", ".join([w.name for w in exists_weapons])}"
            )
        await self._material_repository.delete(command.material_id)
