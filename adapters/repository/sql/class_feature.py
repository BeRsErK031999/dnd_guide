from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import CharacterClassModel, ClassFeatureModel
from application.repository import ClassFeatureRepository as AppClassFeatureRepository
from domain.class_feature import ClassFeature
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

    async def get_by_id(self, feature_id: UUID) -> ClassFeature:
        async with self.__db_helper.session as session:
            query = select(ClassFeatureModel).where(ClassFeatureModel.id == feature_id)
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[ClassFeature]:
        async with self.__db_helper.session as session:
            query = select(ClassFeatureModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [feature.to_domain() for feature in result]

    async def filter(
        self, filter_by_class_id: UUID | None = None
    ) -> list[ClassFeature]:
        async with self.__db_helper.session as session:
            query = select(ClassFeatureModel)
            if filter_by_class_id is not None:
                query = query.where(
                    ClassFeatureModel.character_class_id == filter_by_class_id
                )
            result = await session.execute(query)
            result = result.scalars().all()
            return [feature.to_domain() for feature in result]

    async def create(self, feature: ClassFeature) -> None:
        async with self.__db_helper.session as session:
            model = ClassFeatureModel.from_domain(feature)
            model.character_class = await session.get_one(
                CharacterClassModel, feature.class_id()
            )
            session.add(model)
            await session.commit()

    async def update(self, feature: ClassFeature) -> None:
        async with self.__db_helper.session as session:
            feature_query = select(ClassFeatureModel).where(
                ClassFeatureModel.id == feature.feature_id()
            )
            model = await session.execute(feature_query)
            model = model.scalar_one()
            old_domain = model.to_domain()
            if old_domain.class_id() != feature.class_id():
                model.character_class = await session.get_one(
                    CharacterClassModel, feature.class_id()
                )
            if old_domain.level() != feature.level():
                model.level = feature.level()
            if old_domain.name() != feature.name():
                model.name = feature.name()
            model.description = feature.description()
            await session.commit()

    async def delete(self, feature_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(ClassFeatureModel).where(ClassFeatureModel.id == feature_id)
            await session.execute(stmt)
            await session.commit()
