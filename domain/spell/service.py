from domain.spell.repository import SpellRepository


class SpellService:
    def __init__(self, spell_repository: SpellRepository) -> None:
        self.__repository = spell_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
