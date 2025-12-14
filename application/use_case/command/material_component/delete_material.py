from application.dto.command.material_component import DeleteMaterialComponentCommand
from application.repository import (
    MaterialComponentRepository,
    SpellRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteMaterialComponentUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        material_repository: MaterialComponentRepository,
        spell_repository: SpellRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._material_repository = material_repository
        self._spell_repository = spell_repository

    async def execute(self, command: DeleteMaterialComponentCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._material_repository.id_exists(command.material_id):
            raise DomainError.not_found(
                f"материала с id {command.material_id} не существует"
            )
        exists_spells = await self._spell_repository.filter(
            filter_by_material_ids=[command.material_id]
        )
        if len(exists_spells) > 0:
            raise DomainError.invalid_data(
                "материал  используется в заклинаниях: "
                f"{[spell.name for spell in exists_spells]}"
            )
        await self._material_repository.delete(command.material_id)
