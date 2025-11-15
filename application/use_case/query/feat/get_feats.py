from application.repository import FeatRepository
from domain.feat import Feat


class GetFeatsUseCase:
    def __init__(self, feat_repository: FeatRepository):
        self.__repository = feat_repository

    async def execute(self) -> list[Feat]:
        return await self.__repository.get_all()
