from domain.character_subclass.repository import SubclassRepository


class SubclassService:
    def __init__(self, subclass_repository: SubclassRepository) -> None:
        self._repository = subclass_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)
