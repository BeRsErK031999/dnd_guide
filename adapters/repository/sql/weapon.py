from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    MaterialModel,
    RelWeaponPropertyModel,
    WeaponKindModel,
    WeaponModel,
    WeaponPropertyModel,
)
from application.dto.model.weapon import AppWeapon
from application.repository import WeaponRepository as AppWeaponRepository
from domain.error import DomainError
from domain.weapon import WeaponRepository as DomainWeaponRepository
from sqlalchemy import delete, exists, or_, select
from sqlalchemy.orm import selectinload


class SQLWeaponRepository(DomainWeaponRepository, AppWeaponRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists(WeaponModel)).where(WeaponModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, weapon_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(WeaponModel)).where(WeaponModel.id == weapon_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, weapon_id: UUID) -> AppWeapon:
        async with self.__helper.session as session:
            weapon_query = (
                select(WeaponModel)
                .where(WeaponModel.id == weapon_id)
                .options(selectinload(WeaponModel.properties))
            )
            weapon = await session.execute(weapon_query)
            weapon = weapon.scalar_one()
            return weapon.to_app()

    async def get_all(self) -> list[AppWeapon]:
        async with self.__helper.session as session:
            weapons_query = select(WeaponModel).options(
                selectinload(WeaponModel.properties)
            )
            weapons = await session.execute(weapons_query)
            weapons = weapons.scalars().all()
            return [w.to_app() for w in weapons]

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_kind_ids: list[UUID] | None = None,
        filter_by_damage_types: list[str] | None = None,
        filter_by_property_ids: list[UUID] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> list[AppWeapon]:
        async with self.__helper.session as session:
            query = select(WeaponModel).options(selectinload(WeaponModel.properties))
            conditions = list()
            if search_by_name is not None:
                conditions.append(WeaponModel.name.ilike(f"%{search_by_name}%"))
            if filter_by_kind_ids is not None:
                conditions.append(WeaponModel.kind_id.in_(filter_by_kind_ids))
            if filter_by_damage_types is not None:
                conditions.append(WeaponModel.damage_type.in_(filter_by_damage_types))
            if filter_by_property_ids is not None:
                conditions.append(
                    WeaponModel.properties.any(
                        RelWeaponPropertyModel.weapon_property_id.in_(
                            filter_by_property_ids
                        )
                    )
                )
            if filter_by_material_ids is not None:
                conditions.append(WeaponModel.material_id.in_(filter_by_material_ids))
            if len(conditions) > 0:
                query = query.where(or_(*conditions))
            weapons = await session.execute(query)
            weapons = weapons.scalars().all()
            return [w.to_app() for w in weapons]

    async def create(self, weapon: AppWeapon) -> None:
        async with self.__helper.session as session:
            model = WeaponModel.from_app(weapon)
            model.kind = await session.get_one(WeaponKindModel, weapon.weapon_kind_id)
            model.material = await session.get_one(MaterialModel, weapon.material_id)
            await session.flush()
            if len(weapon.weapon_property_ids) > 0:
                property_query = select(WeaponPropertyModel).where(
                    WeaponPropertyModel.id.in_(weapon.weapon_property_ids)
                )
                property_model = await session.execute(property_query)
                property_model = property_model.scalars().all()
                if len(weapon.weapon_property_ids) != len(property_model):
                    not_exists_ids = set(weapon.weapon_property_ids) - set(
                        [p.id for p in property_model]
                    )
                    raise DomainError.invalid_data(
                        f"свойств не существует, id: {not_exists_ids}"
                    )
                model.properties.extend(property_model)
            await session.commit()

    async def update(self, weapon: AppWeapon) -> None:
        async with self.__helper.session as session:
            query = (
                select(WeaponModel)
                .where(WeaponModel.id == weapon.weapon_id)
                .options(selectinload(WeaponModel.properties))
            )
            model = await session.execute(query)
            model = model.scalar_one()
            old = model.to_app()
            if old.weapon_kind_id != weapon.weapon_kind_id:
                model.kind = await session.get_one(
                    WeaponKindModel, weapon.weapon_kind_id
                )
            if old.cost != weapon.cost:
                model.cost = weapon.cost.count
            if old.damage != weapon.damage:
                damage_dice = weapon.damage.dice
                model.damage_type = weapon.damage.damage_type
                model.damage_dice_name = damage_dice.dice_type
                model.damage_dice_count = damage_dice.count
            if old.weight != weapon.weight:
                model.weight = weapon.weight.count
            if old.material_id != weapon.material_id:
                model.material = await session.get_one(
                    MaterialModel, weapon.material_id
                )
            property_query = select(WeaponPropertyModel).where(
                WeaponPropertyModel.id.in_(weapon.weapon_property_ids)
            )
            property_model = await session.execute(property_query)
            property_model = property_model.scalars().all()
            if len(weapon.weapon_property_ids) != len(property_model):
                not_exists_ids = set(weapon.weapon_property_ids) - set(
                    [p.id for p in property_model]
                )
                raise DomainError.invalid_data(
                    f"свойств не существует, id: {not_exists_ids}"
                )
            model.properties.clear()
            model.properties.extend(property_model)
            await session.commit()

    async def delete(self, weapon_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(WeaponModel).where(WeaponModel.id == weapon_id)
            await session.execute(stmt)
            await session.commit()
