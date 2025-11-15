from application.dto.query.spell import SpellQuery
from application.repository import SpellRepository
from domain.error import DomainError
from domain.spell import Spell


class GetSpellUseCase:
    def __init__(self, spell_repository: SpellRepository):
        self.__repository = spell_repository

    async def execute(self, query: SpellQuery) -> Spell:
        if not await self.__repository.id_exists(query.spell_id):
            raise DomainError.not_found(
                f"заклинания с id {query.spell_id} не существует"
            )
        return await self.__repository.get_by_id(query.spell_id)
