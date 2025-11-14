from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    FeatIncreaseModifierModel,
    FeatModel,
    FeatRequiredArmorTypeModel,
    FeatRequiredModifierModel,
)
from application.repository import FeatRepository as AppFeatRepository
from domain.feat import FeatRepository as DomainFeatRepository
from domain.feat.feat import Feat
from sqlalchemy import delete, exists, select
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

    async def get_by_id(self, feat_id: UUID) -> Feat:
        async with self.__helper.session as session:
            query = (
                select(FeatModel)
                .where(FeatModel.id == feat_id)
                .options(
                    selectinload(
                        FeatModel.required_armor_types,
                        FeatModel.required_modifiers,
                        FeatModel.increase_modifiers,
                    )
                )
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[Feat]:
        async with self.__helper.session as session:
            query = select(FeatModel).options(
                selectinload(
                    FeatModel.required_armor_types,
                    FeatModel.required_modifiers,
                    FeatModel.increase_modifiers,
                )
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_domain() for item in result]

    async def create(self, feat: Feat) -> None:
        async with self.__helper.session as session:
            model = FeatModel.from_domain(feat)
            if len(feat.increase_modifiers()) > 0:
                model.increase_modifiers.extend(
                    [
                        FeatIncreaseModifierModel.from_domain(feat.feat_id(), modifier)
                        for modifier in feat.increase_modifiers()
                    ]
                )
            if len(feat.required_armor_types()) > 0:
                model.required_armor_types.extend(
                    [
                        FeatRequiredArmorTypeModel.from_domain(
                            feat.feat_id(), armor_type
                        )
                        for armor_type in feat.required_armor_types()
                    ]
                )
            if len(feat.required_modifiers()) > 0:
                model.required_modifiers.extend(
                    [
                        FeatRequiredModifierModel.from_domain(feat.feat_id(), modifier)
                        for modifier in feat.required_modifiers()
                    ]
                )
            session.add(model)
            await session.commit()

    async def update(self, feat: Feat) -> None:
        async with self.__helper.session as session:
            feat_query = (
                select(FeatModel)
                .where(FeatModel.id == feat.feat_id())
                .options(
                    selectinload(
                        FeatModel.required_armor_types,
                        FeatModel.required_modifiers,
                        FeatModel.increase_modifiers,
                    )
                )
            )
            model = await session.execute(feat_query)
            model = model.scalar_one()
            old_domain = model.to_domain()
            if old_domain.name() != feat.name():
                model.name = feat.name()
            if old_domain.is_caster() != feat.is_caster():
                model.is_caster = feat.is_caster()
            model.description = feat.description()
            model.increase_modifiers.clear()
            if len(feat.increase_modifiers()) > 0:
                model.increase_modifiers.extend(
                    [
                        FeatIncreaseModifierModel.from_domain(feat.feat_id(), modifier)
                        for modifier in feat.increase_modifiers()
                    ]
                )
            model.required_armor_types.clear()
            if len(feat.required_armor_types()) > 0:
                model.required_armor_types.extend(
                    [
                        FeatRequiredArmorTypeModel.from_domain(
                            feat.feat_id(), armor_type
                        )
                        for armor_type in feat.required_armor_types()
                    ]
                )
            model.required_modifiers.clear()
            if len(feat.required_modifiers()) > 0:
                model.required_modifiers.extend(
                    [
                        FeatRequiredModifierModel.from_domain(feat.feat_id(), modifier)
                        for modifier in feat.required_modifiers()
                    ]
                )
            await session.commit()

    async def delete(self, feat_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(FeatModel).where(FeatModel.id == feat_id)
            await session.execute(stmt)
            await session.commit()
