from .repository import MaterialRepository


class MaterialService:
    def __init__(self, material_repository: MaterialRepository) -> None:
        self._repository = material_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)
