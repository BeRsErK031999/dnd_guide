from domain.material_component.repository import MaterialComponentRepository


class MaterialComponentService:
    def __init__(
        self, material_component_repository: MaterialComponentRepository
    ) -> None:
        self.__repository = material_component_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)
