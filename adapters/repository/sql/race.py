from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    CreatureSizeModel,
    CreatureTypeModel,
    RaceFeatureModel,
    RaceIncreaseModifierModel,
    RaceModel,
    SourceModel,
)
from application.repository import RaceRepository as AppRaceRepository
from domain.race import Race
from domain.race import RaceRepository as DomainRaceRepository
from sqlalchemy import delete, exists, select
from sqlalchemy.orm import selectinload


class SQLRaceRepository(DomainRaceRepository, AppRaceRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(RaceModel)).where(RaceModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, race_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(RaceModel)).where(RaceModel.id == race_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, race_id: UUID) -> Race:
        async with self.__db_helper.session as session:
            query = (
                select(RaceModel)
                .where(RaceModel.id == race_id)
                .options(
                    selectinload(RaceModel.increase_modifiers),
                    selectinload(RaceModel.features),
                )
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[Race]:
        async with self.__db_helper.session as session:
            query = select(RaceModel).options(
                selectinload(RaceModel.increase_modifiers),
                selectinload(RaceModel.features),
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_domain() for item in result]

    async def create(self, race: Race) -> None:
        async with self.__db_helper.session as session:
            model = RaceModel.from_domain(race)
            model.source = await session.get_one(SourceModel, race.source_id())
            model.creature_size = await session.get_one(
                CreatureSizeModel, race.size_id()
            )
            model.creature_type = await session.get_one(
                CreatureTypeModel, race.type_id()
            )
            model.increase_modifiers.extend(
                [
                    RaceIncreaseModifierModel.from_domain(race.race_id(), im)
                    for im in race.increase_modifiers()
                ]
            )
            model.features.extend(
                [
                    RaceFeatureModel.from_domain(race.race_id(), f)
                    for f in race.features()
                ]
            )
            session.add(model)
            await session.commit()

    async def update(self, race: Race) -> None:
        async with self.__db_helper.session as session:
            race_query = (
                select(RaceModel)
                .where(RaceModel.id == race.race_id())
                .options(
                    selectinload(RaceModel.increase_modifiers),
                    selectinload(RaceModel.features),
                )
            )
            model = await session.execute(race_query)
            model = model.scalar_one()
            old_domain = model.to_domain()
            if old_domain.type_id() != race.type_id():
                model.creature_type = await session.get_one(
                    CreatureTypeModel, race.type_id()
                )
            if old_domain.size_id() != race.size_id():
                model.creature_size = await session.get_one(
                    CreatureSizeModel, race.size_id()
                )
            if old_domain.speed() != race.speed():
                model.base_speed = race.speed().base_speed().in_ft()
                model.speed_description = race.speed().description()
            if old_domain.age() != race.age():
                model.max_age = race.age().max_age()
                model.age_description = race.age().description()
            if old_domain.name() != race.name():
                model.name = race.name()
            if old_domain.name_in_english() != race.name_in_english():
                model.name_in_english = race.name_in_english()
            if old_domain.source_id() != race.source_id():
                model.source = await session.get_one(SourceModel, race.source_id())
            model.description = race.description()
            model.increase_modifiers.clear()
            model.increase_modifiers.extend(
                [
                    RaceIncreaseModifierModel.from_domain(race.race_id(), im)
                    for im in race.increase_modifiers()
                ]
            )
            model.features.clear()
            model.features.extend(
                [
                    RaceFeatureModel.from_domain(race.race_id(), f)
                    for f in race.features()
                ]
            )
            await session.commit()

    async def delete(self, race_id: UUID) -> None:
        async with self.__db_helper.session as session:
            query = delete(RaceModel).where(RaceModel.id == race_id)
            await session.execute(query)
            await session.commit()
