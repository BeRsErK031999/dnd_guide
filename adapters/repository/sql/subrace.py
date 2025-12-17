from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    RaceModel,
    SubraceFeatureModel,
    SubraceIncreaseModifierModel,
    SubraceModel,
)
from application.dto.model.subrace import AppSubrace
from application.repository import SubraceRepository as AppSubraceRepository
from domain.subrace import SubraceRepository as DomainSubraceRepository
from sqlalchemy import Select, delete, exists, or_, select
from sqlalchemy.orm import selectinload


class SQLSubraceRepository(DomainSubraceRepository, AppSubraceRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(SubraceModel)).where(SubraceModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, subrace_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(SubraceModel)).where(SubraceModel.id == subrace_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, subrace_id: UUID) -> AppSubrace:
        async with self.__db_helper.session as session:
            query = self._add_options(
                select(SubraceModel).where(SubraceModel.id == subrace_id)
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_app()

    async def get_all(self) -> list[AppSubrace]:
        async with self.__db_helper.session as session:
            query = self._add_options(select(SubraceModel))
            result = await session.execute(query)
            result = result.scalars().all()
            return [r.to_app() for r in result]

    async def filter(self, search_by_name: str | None = None) -> list[AppSubrace]:
        async with self.__db_helper.session as session:
            query = self._add_options(select(SubraceModel))
            if search_by_name is not None:
                query = query.where(
                    or_(
                        SubraceModel.name.ilike(f"%{search_by_name}%"),
                        SubraceModel.name_in_english.ilike(f"%{search_by_name}%"),
                    )
                )
            result = await session.execute(query)
            result = result.scalars().all()
            return [r.to_app() for r in result]

    async def save(self, subrace: AppSubrace) -> None:
        if await self.id_exists(subrace.subrace_id):
            await self.update(subrace)
        await self.create(subrace)

    async def create(self, subrace: AppSubrace) -> None:
        async with self.__db_helper.session as session:
            model = SubraceModel.from_domain(subrace)
            model.increase_modifiers.extend(
                [
                    SubraceIncreaseModifierModel.from_app(im)
                    for im in subrace.increase_modifiers
                ]
            )
            model.features.extend(
                [SubraceFeatureModel.from_app(f) for f in subrace.features]
            )
            session.add(model)
            await session.commit()

    async def update(self, subrace: AppSubrace) -> None:
        async with self.__db_helper.session as session:
            subrace_query = self._add_options(
                select(SubraceModel).where(SubraceModel.id == subrace.subrace_id)
            )
            model = await session.execute(subrace_query)
            model = model.scalar_one()
            old = model.to_app()
            if old.race_id != subrace.race_id:
                model.race = await session.get_one(RaceModel, subrace.race_id)
            if old.name != subrace.name:
                model.name = subrace.name
            if old.name_in_english != subrace.name_in_english:
                model.name_in_english = subrace.name_in_english
            model.description = subrace.description
            model.increase_modifiers.clear()
            model.increase_modifiers.extend(
                [
                    SubraceIncreaseModifierModel.from_app(im)
                    for im in subrace.increase_modifiers
                ]
            )
            model.features.clear()
            model.features.extend(
                [SubraceFeatureModel.from_app(f) for f in subrace.features]
            )
            await session.commit()

    async def delete(self, subrace_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(SubraceModel).where(SubraceModel.id == subrace_id)
            await session.execute(stmt)
            await session.commit()

    def _add_options(
        self, query: Select[tuple[SubraceModel]]
    ) -> Select[tuple[SubraceModel]]:
        return query.options(
            selectinload(SubraceModel.increase_modifiers),
            selectinload(SubraceModel.features),
        )
