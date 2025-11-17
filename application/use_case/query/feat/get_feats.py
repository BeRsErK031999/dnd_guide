from application.dto.query.feat import FeatsQuery
from application.repository import FeatRepository
from domain.feat import Feat


class GetFeatsUseCase:
    def __init__(self, feat_repository: FeatRepository):
        self.__repository = feat_repository

    async def execute(self, query: FeatsQuery) -> list[Feat]:
        return await self.__repository.filter(
            search_by_name=query.search_by_name,
            filter_by_caster=query.filter_by_caster,
            filter_by_required_armor_types=query.filter_by_required_armor_types,
            filter_by_required_modifiers=query.filter_by_required_modifiers,
            filter_by_increase_modifiers=query.filter_by_increase_modifiers,
        )
