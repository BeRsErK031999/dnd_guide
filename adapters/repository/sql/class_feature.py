from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import CharacterClassModel, ClassFeatureModel
from application.dto.model.class_feature import AppClassFeature
from application.repository import ClassFeatureRepository as AppClassFeatureRepository
from domain.class_feature import ClassFeatureRepository as DomainClassFeatureRepository
from sqlalchemy import delete, exists, select


class SQLClassFeatureRepository(
    DomainClassFeatureRepository, AppClassFeatureRepository
):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_for_class_exists(self, class_id: UUID, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(ClassFeatureModel)).where(
                ClassFeatureModel.character_class_id == class_id,
                ClassFeatureModel.name == name,
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, feature_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(ClassFeatureModel)).where(
                ClassFeatureModel.id == feature_id
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, feature_id: UUID) -> AppClassFeature:
        async with self.__db_helper.session as session:
            query = select(ClassFeatureModel).where(ClassFeatureModel.id == feature_id)
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_app()

    async def get_all(self) -> list[AppClassFeature]:
        async with self.__db_helper.session as session:
            query = select(ClassFeatureModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [feature.to_app() for feature in result]

    async def filter(
        self, filter_by_class_id: UUID | None = None
    ) -> list[AppClassFeature]:
        async with self.__db_helper.session as session:
            query = select(ClassFeatureModel)
            if filter_by_class_id is not None:
                query = query.where(
                    ClassFeatureModel.character_class_id == filter_by_class_id
                )
            result = await session.execute(query)
            result = result.scalars().all()
            return [feature.to_app() for feature in result]

    async def save(self, feature: AppClassFeature) -> None:
        if await self.id_exists(feature.feature_id):
            await self.update(feature)
        await self.create(feature)

    async def create(self, feature: AppClassFeature) -> None:
        async with self.__db_helper.session as session:
            model = ClassFeatureModel.from_app(feature)
            model.character_class = await session.get_one(
                CharacterClassModel, feature.class_id
            )
            session.add(model)
            await session.commit()

    async def update(self, feature: AppClassFeature) -> None:
        async with self.__db_helper.session as session:
            feature_query = select(ClassFeatureModel).where(
                ClassFeatureModel.id == feature.feature_id
            )
            model = await session.execute(feature_query)
            model = model.scalar_one()
            old = model.to_app()
            if old.class_id != feature.class_id:
                model.character_class = await session.get_one(
                    CharacterClassModel, feature.class_id
                )
            if old.level != feature.level:
                model.level = feature.level
            if old.name != feature.name:
                model.name = feature.name
            model.description = feature.description
            await session.commit()

    async def delete(self, feature_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(ClassFeatureModel).where(ClassFeatureModel.id == feature_id)
            await session.execute(stmt)
            await session.commit()
