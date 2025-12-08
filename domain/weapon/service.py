from domain.weapon.repository import WeaponRepository


class WeaponService:
    def __init__(self, weapon_repository: WeaponRepository) -> None:
        self._repository = weapon_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)
