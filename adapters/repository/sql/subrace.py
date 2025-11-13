from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    RaceModel,
    SubraceFeatureModel,
    SubraceIncreaseModifierModel,
    SubraceModel,
)
from application.repository import SubraceRepository as AppSubraceRepository
from domain.subrace import Subrace
from domain.subrace import SubraceRepository as DomainSubraceRepository
from sqlalchemy import delete, exists, select
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

    async def get_by_id(self, subrace_id: UUID) -> Subrace:
        async with self.__db_helper.session as session:
            query = (
                select(SubraceModel)
                .where(SubraceModel.id == subrace_id)
                .options(
                    selectinload(SubraceModel.increase_modifiers, SubraceModel.features)
                )
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[Subrace]:
        async with self.__db_helper.session as session:
            query = select(SubraceModel).options(
                selectinload(SubraceModel.increase_modifiers, SubraceModel.features)
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [r.to_domain() for r in result]

    async def create(self, subrace: Subrace) -> None:
        async with self.__db_helper.session as session:
            model = SubraceModel.from_domain(subrace)
            model.increase_modifiers.extend(
                [
                    SubraceIncreaseModifierModel.from_domain(im)
                    for im in subrace.increase_modifiers()
                ]
            )
            model.features.extend(
                [SubraceFeatureModel.from_domain(f) for f in subrace.features()]
            )
            session.add(model)
            await session.commit()

    async def update(self, subrace: Subrace) -> None:
        async with self.__db_helper.session as session:
            subrace_query = (
                select(SubraceModel)
                .where(SubraceModel.id == subrace.subrace_id())
                .options(
                    selectinload(SubraceModel.increase_modifiers, SubraceModel.features)
                )
            )
            model = await session.execute(subrace_query)
            model = model.scalar_one()
            old_domain = model.to_domain()
            if old_domain.race_id() != subrace.race_id():
                model.race = await session.get_one(RaceModel, subrace.race_id())
            if old_domain.name() != subrace.name():
                model.name = subrace.name()
            if old_domain.name_in_english() != subrace.name_in_english():
                model.name_in_english = subrace.name_in_english()
            model.description = subrace.description()
            model.increase_modifiers.clear()
            model.increase_modifiers.extend(
                [
                    SubraceIncreaseModifierModel.from_domain(im)
                    for im in subrace.increase_modifiers()
                ]
            )
            model.features.clear()
            model.features.extend(
                [SubraceFeatureModel.from_domain(f) for f in subrace.features()]
            )
            await session.commit()

    async def delete(self, subrace_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(SubraceModel).where(SubraceModel.id == subrace_id)
            await session.execute(stmt)
            await session.commit()
