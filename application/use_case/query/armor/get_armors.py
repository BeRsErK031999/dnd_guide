from application.repository import ArmorRepository
from domain.armor import Armor


class GetArmorsUseCase:
    def __init__(self, armor_repository: ArmorRepository):
        self.__repository = armor_repository

    async def execute(self) -> list[Armor]:
        return await self.__repository.get_all()
