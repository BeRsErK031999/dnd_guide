from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import WeaponPropertyModel
from application.repository import (
    WeaponPropertyRepository as AppWeaponPropertyRepository,
)
from domain.weapon_property import WeaponProperty
from domain.weapon_property import (
    WeaponPropertyRepository as DomainWeaponPropertyRepository,
)
from sqlalchemy import delete, exists, select


class SQLWeaponPropertyRepository(
    DomainWeaponPropertyRepository, AppWeaponPropertyRepository
):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists(WeaponPropertyModel)).where(
                WeaponPropertyModel.name == name
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, weapon_property_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(WeaponPropertyModel)).where(
                WeaponPropertyModel.id == weapon_property_id
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, weapon_property_id: UUID) -> WeaponProperty:
        async with self.__helper.session as session:
            query = select(WeaponPropertyModel).where(
                WeaponPropertyModel.id == weapon_property_id
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[WeaponProperty]:
        async with self.__helper.session as session:
            query = select(WeaponPropertyModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_domain() for item in result]

    async def create(self, weapon_property: WeaponProperty) -> None:
        async with self.__helper.session as session:
            session.add(WeaponPropertyModel.from_domain(weapon_property))
            await session.commit()

    async def update(self, weapon_property: WeaponProperty) -> None:
        async with self.__helper.session as session:
            query = select(WeaponPropertyModel).where(
                WeaponPropertyModel.id == weapon_property.weapon_property_id()
            )
            result = await session.execute(query)
            model = result.scalar_one()
            old_domain = model.to_domain()
            if old_domain.name() != weapon_property.name():
                model.name = weapon_property.name()
            if old_domain.base_range() != weapon_property.base_range():
                base_range = weapon_property.base_range()
                model.base_range = (
                    base_range.in_ft() if base_range is not None else None
                )
            if old_domain.max_range() != weapon_property.max_range():
                max_range = weapon_property.max_range()
                model.max_range = max_range.in_ft() if max_range is not None else None
            if old_domain.second_hand_dice() != weapon_property.second_hand_dice():
                second_hand_dice = weapon_property.second_hand_dice()
                model.second_hand_dice_name = (
                    second_hand_dice.dice_type().name
                    if second_hand_dice is not None
                    else None
                )
                model.second_hand_dice_count = (
                    second_hand_dice.count() if second_hand_dice is not None else None
                )
            await session.commit()

    async def delete(self, weapon_property_id: UUID) -> None:
        async with self.__helper.session as session:
            query = delete(WeaponPropertyModel).where(
                WeaponPropertyModel.id == weapon_property_id
            )
            await session.execute(query)
            await session.commit()
