from application.repository import SpellRepository
from domain.spell import Spell


class GetSpellsUseCase:
    def __init__(self, spell_repository: SpellRepository):
        self.__repository = spell_repository

    async def execute(self) -> list[Spell]:
        return await self.__repository.get_all()
