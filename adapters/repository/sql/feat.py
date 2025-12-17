from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    FeatIncreaseModifierModel,
    FeatModel,
    FeatRequiredArmorTypeModel,
    FeatRequiredModifierModel,
)
from application.dto.model.feat import AppFeat
from application.repository import FeatRepository as AppFeatRepository
from domain.feat import FeatRepository as DomainFeatRepository
from sqlalchemy import Select, delete, exists, select
from sqlalchemy.orm import selectinload


class SQLFeatRepository(DomainFeatRepository, AppFeatRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists(FeatModel)).where(FeatModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, feat_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(FeatModel)).where(FeatModel.id == feat_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, feat_id: UUID) -> AppFeat:
        async with self.__helper.session as session:
            query = self._add_options(select(FeatModel).where(FeatModel.id == feat_id))
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_app()

    async def get_all(self) -> list[AppFeat]:
        async with self.__helper.session as session:
            query = self._add_options(select(FeatModel))
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_caster: bool | None = None,
        filter_by_required_armor_types: list[str] | None = None,
        filter_by_required_modifiers: list[str] | None = None,
        filter_by_increase_modifiers: list[str] | None = None,
    ) -> list[AppFeat]:
        async with self.__helper.session as session:
            query = self._add_options(select(FeatModel))
            conditions = list()
            if search_by_name is not None:
                conditions.append(FeatModel.name.ilike(f"%{search_by_name}%"))
            if filter_by_caster is not None:
                conditions.append(FeatModel.caster == filter_by_caster)
            if filter_by_required_armor_types is not None:
                conditions.append(
                    FeatModel.required_armor_types.any(
                        FeatRequiredArmorTypeModel.name.in_(
                            filter_by_required_armor_types
                        )
                    )
                )
            if filter_by_required_modifiers is not None:
                conditions.append(
                    FeatModel.required_modifiers.any(
                        FeatRequiredModifierModel.name.in_(filter_by_required_modifiers)
                    )
                )
            if filter_by_increase_modifiers is not None:
                conditions.append(
                    FeatModel.increase_modifiers.any(
                        FeatIncreaseModifierModel.name.in_(filter_by_increase_modifiers)
                    )
                )
            if len(conditions) > 0:
                query = query.where(*conditions)
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def save(self, feat: AppFeat) -> None:
        if await self.id_exists(feat.feat_id):
            await self.update(feat)
        else:
            await self.create(feat)

    async def create(self, feat: AppFeat) -> None:
        async with self.__helper.session as session:
            model = FeatModel.from_app(feat)
            if len(feat.increase_modifiers) > 0:
                model.increase_modifiers.extend(
                    [
                        FeatIncreaseModifierModel.from_app(feat.feat_id, m)
                        for m in feat.increase_modifiers
                    ]
                )
            if len(feat.required_armor_types) > 0:
                model.required_armor_types.extend(
                    [
                        FeatRequiredArmorTypeModel.from_app(feat.feat_id, t)
                        for t in feat.required_armor_types
                    ]
                )
            if len(feat.required_modifiers) > 0:
                model.required_modifiers.extend(
                    [
                        FeatRequiredModifierModel.from_app(feat.feat_id, m)
                        for m in feat.required_modifiers
                    ]
                )
            session.add(model)
            await session.commit()

    async def update(self, feat: AppFeat) -> None:
        async with self.__helper.session as session:
            feat_query = self._add_options(
                select(FeatModel).where(FeatModel.id == feat.feat_id)
            )
            model = await session.execute(feat_query)
            model = model.scalar_one()
            old = model.to_app()
            if old.name != feat.name:
                model.name = feat.name
            if old.caster != feat.caster:
                model.caster = feat.caster
            model.description = feat.description
            model.increase_modifiers.clear()
            if len(feat.increase_modifiers) > 0:
                model.increase_modifiers.extend(
                    [
                        FeatIncreaseModifierModel.from_app(feat.feat_id, m)
                        for m in feat.increase_modifiers
                    ]
                )
            model.required_armor_types.clear()
            if len(feat.required_armor_types) > 0:
                model.required_armor_types.extend(
                    [
                        FeatRequiredArmorTypeModel.from_app(feat.feat_id, t)
                        for t in feat.required_armor_types
                    ]
                )
            model.required_modifiers.clear()
            if len(feat.required_modifiers) > 0:
                model.required_modifiers.extend(
                    [
                        FeatRequiredModifierModel.from_app(feat.feat_id, m)
                        for m in feat.required_modifiers
                    ]
                )
            await session.commit()

    async def delete(self, feat_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(FeatModel).where(FeatModel.id == feat_id)
            await session.execute(stmt)
            await session.commit()

    def _add_options(self, query: Select[tuple[FeatModel]]) -> Select[tuple[FeatModel]]:
        return query.options(
            selectinload(FeatModel.required_armor_types),
            selectinload(FeatModel.required_modifiers),
            selectinload(FeatModel.increase_modifiers),
        )
