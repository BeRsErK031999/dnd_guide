from application.repository import WeaponRepository
from domain.weapon import Weapon


class GetWeaponsUseCase:
    def __init__(self, weapon_repository: WeaponRepository):
        self.__repository = weapon_repository

    async def execute(self) -> list[Weapon]:
        return await self.__repository.get_all()
