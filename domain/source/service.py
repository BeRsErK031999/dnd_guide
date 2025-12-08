from domain.source.repository import SourceRepository


class SourceService:
    def __init__(self, source_repository: SourceRepository) -> None:
        self._repository = source_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)
