from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import CharacterSubclassModel, SubclassFeatureModel
from application.dto.model.subclass_feature import AppSubclassFeature
from application.repository import (
    SubclassFeatureRepository as AppSubclassFeatureRepository,
)
from domain.subclass_feature import (
    SubclassFeatureRepository as DomainSubclassFeatureRepository,
)
from sqlalchemy import delete, exists, select
from sqlalchemy.orm import selectinload


class SQLSubclassFeatureRepository(
    DomainSubclassFeatureRepository, AppSubclassFeatureRepository
):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_for_subclass_exists(self, subclass_id: UUID, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(SubclassFeatureModel)).where(
                SubclassFeatureModel.name == name,
                SubclassFeatureModel.character_subclass_id == subclass_id,
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, feature_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(SubclassFeatureModel)).where(
                SubclassFeatureModel.id == feature_id
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, feature_id: UUID) -> AppSubclassFeature:
        async with self.__db_helper.session as session:
            query = (
                select(SubclassFeatureModel)
                .where(SubclassFeatureModel.id == feature_id)
                .options(selectinload(SubclassFeatureModel.character_subclass))
            )
            result = await session.execute(query)
            model = result.scalar_one()
            return model.to_app()

    async def get_all(self) -> list[AppSubclassFeature]:
        async with self.__db_helper.session as session:
            query = select(SubclassFeatureModel).options(
                selectinload(SubclassFeatureModel.character_subclass)
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [model.to_app() for model in result]

    async def filter(
        self, filter_by_subclass_id: UUID | None = None
    ) -> list[AppSubclassFeature]:
        async with self.__db_helper.session as session:
            query = select(SubclassFeatureModel).options(
                selectinload(SubclassFeatureModel.character_subclass)
            )
            if filter_by_subclass_id is not None:
                query = query.where(
                    SubclassFeatureModel.character_subclass_id == filter_by_subclass_id
                )
            result = await session.execute(query)
            result = result.scalars().all()
            return [model.to_app() for model in result]

    async def save(self, feature: AppSubclassFeature) -> None:
        if await self.id_exists(feature.feature_id):
            await self.update(feature)
        else:
            await self.create(feature)

    async def create(self, feature: AppSubclassFeature) -> None:
        async with self.__db_helper.session as session:
            session.add(SubclassFeatureModel.from_app(feature))
            await session.commit()

    async def update(self, feature: AppSubclassFeature) -> None:
        async with self.__db_helper.session as session:
            feature_query = (
                select(SubclassFeatureModel)
                .where(SubclassFeatureModel.id == feature.feature_id)
                .options(selectinload(SubclassFeatureModel.character_subclass))
            )
            model = await session.execute(feature_query)
            model = model.scalar_one()
            old_domain = model.to_app()
            if old_domain.subclass_id != feature.subclass_id:
                model.character_subclass = await session.get_one(
                    CharacterSubclassModel, feature.subclass_id
                )
            if old_domain.level != feature.level:
                model.level = feature.level
            if old_domain.name != feature.name:
                model.name = feature.name
            if old_domain.name_in_english != feature.name_in_english:
                model.name_in_english = feature.name_in_english
            model.description = feature.description
            await session.commit()

    async def delete(self, feature_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(SubclassFeatureModel).where(
                SubclassFeatureModel.id == feature_id
            )
            await session.execute(stmt)
            await session.commit()
