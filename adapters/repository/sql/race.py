from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    RaceFeatureModel,
    RaceIncreaseModifierModel,
    RaceModel,
    SourceModel,
)
from application.dto.model.race import AppRace
from application.repository import RaceRepository as AppRaceRepository
from domain.error import DomainError
from domain.race import RaceRepository as DomainRaceRepository
from sqlalchemy import Select, delete, exists, or_, select
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

    async def get_by_id(self, race_id: UUID) -> AppRace:
        async with self.__db_helper.session as session:
            query = self._add_options(select(RaceModel).where(RaceModel.id == race_id))
            result = await session.execute(query)
            result = result.scalar()
            if result is None:
                raise DomainError.not_found(f"раса с id {race_id} не существует")
            return result.to_app()

    async def get_all(self) -> list[AppRace]:
        async with self.__db_helper.session as session:
            query = self._add_options(select(RaceModel))
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_source_ids: list[UUID] | None = None,
    ) -> list[AppRace]:
        async with self.__db_helper.session as session:
            query = self._add_options(select(RaceModel))
            if search_by_name is not None:
                query = query.where(
                    or_(
                        RaceModel.name.ilike(f"%{search_by_name}%"),
                        RaceModel.name_in_english.ilike(f"%{search_by_name}%"),
                    )
                )
            if filter_by_source_ids is not None:
                query = query.where(RaceModel.source_id.in_(filter_by_source_ids))
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def save(self, race: AppRace) -> None:
        if await self.id_exists(race.race_id):
            await self.update(race)
        else:
            await self.create(race)

    async def create(self, race: AppRace) -> None:
        async with self.__db_helper.session as session:
            model = RaceModel.from_app(race)
            model.source = await session.get_one(SourceModel, race.source_id)
            model.creature_size = race.creature_size
            model.creature_type = race.creature_type
            model.increase_modifiers.extend(
                [
                    RaceIncreaseModifierModel.from_app(race.race_id, im)
                    for im in race.increase_modifiers
                ]
            )
            model.features.extend(
                [RaceFeatureModel.from_app(race.race_id, f) for f in race.features]
            )
            session.add(model)
            await session.commit()

    async def update(self, race: AppRace) -> None:
        async with self.__db_helper.session as session:
            race_query = self._add_options(
                select(RaceModel).where(RaceModel.id == race.race_id)
            )
            model = await session.execute(race_query)
            model = model.scalar_one()
            old = model.to_app()
            if old.creature_type != race.creature_type:
                model.creature_type = race.creature_type
            if old.creature_size != race.creature_size:
                model.creature_size = race.creature_size
            if old.speed != race.speed:
                model.base_speed = race.speed.base_speed.count
                model.speed_description = race.speed.description
            if old.age != race.age:
                model.max_age = race.age.max_age
                model.age_description = race.age.description
            if old.name != race.name:
                model.name = race.name
            if old.name_in_english != race.name_in_english:
                model.name_in_english = race.name_in_english
            if old.source_id != race.source_id:
                model.source = await session.get_one(SourceModel, race.source_id)
            model.description = race.description
            model.increase_modifiers.clear()
            model.increase_modifiers.extend(
                [
                    RaceIncreaseModifierModel.from_app(race.race_id, im)
                    for im in race.increase_modifiers
                ]
            )
            model.features.clear()
            model.features.extend(
                [RaceFeatureModel.from_app(race.race_id, f) for f in race.features]
            )
            await session.commit()

    async def delete(self, race_id: UUID) -> None:
        async with self.__db_helper.session as session:
            query = delete(RaceModel).where(RaceModel.id == race_id)
            result = await session.execute(query)
            if result.rowcount == 0:
                raise DomainError.not_found(f"раса с id {race_id} не существует")
            await session.commit()

    def _add_options(self, query: Select[tuple[RaceModel]]) -> Select[tuple[RaceModel]]:
        return query.options(
            selectinload(RaceModel.increase_modifiers),
            selectinload(RaceModel.features),
        )
