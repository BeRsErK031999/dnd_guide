from application.repository import WeaponKindRepository
from domain.weapon_kind import WeaponKind


class GetWeaponKindsUseCase:
    def __init__(self, weapon_kind_repository: WeaponKindRepository):
        self.__repository = weapon_kind_repository

    async def execute(self) -> list[WeaponKind]:
        return await self.__repository.get_all()
