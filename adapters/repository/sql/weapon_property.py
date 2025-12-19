from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import WeaponPropertyModel
from application.dto.model.weapon_property import AppWeaponProperty
from application.repository import (
    WeaponPropertyRepository as AppWeaponPropertyRepository,
)
from domain.error import DomainError
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

    async def get_by_id(self, weapon_property_id: UUID) -> AppWeaponProperty:
        async with self.__helper.session as session:
            query = select(WeaponPropertyModel).where(
                WeaponPropertyModel.id == weapon_property_id
            )
            result = await session.execute(query)
            result = result.scalar()
            if result is None:
                raise DomainError.not_found(
                    f"свойства оружия с id {weapon_property_id} не существует"
                )
            return result.to_app()

    async def get_all(self) -> list[AppWeaponProperty]:
        async with self.__helper.session as session:
            query = select(WeaponPropertyModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def filter(
        self, search_by_name: str | None = None
    ) -> list[AppWeaponProperty]:
        async with self.__helper.session as session:
            query = select(WeaponPropertyModel)
            if search_by_name is not None:
                query = query.where(
                    WeaponPropertyModel.name.ilike(f"%{search_by_name}%")
                )
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def save(self, weapon_property: AppWeaponProperty) -> None:
        if await self.id_exists(weapon_property.weapon_property_id):
            await self.update(weapon_property)
        else:
            await self.create(weapon_property)

    async def create(self, weapon_property: AppWeaponProperty) -> None:
        async with self.__helper.session as session:
            session.add(WeaponPropertyModel.from_app(weapon_property))
            await session.commit()

    async def update(self, weapon_property: AppWeaponProperty) -> None:
        async with self.__helper.session as session:
            query = select(WeaponPropertyModel).where(
                WeaponPropertyModel.id == weapon_property.weapon_property_id
            )
            result = await session.execute(query)
            model = result.scalar_one()
            old = model.to_app()
            if old.name != weapon_property.name:
                model.name = weapon_property.name
            if old.base_range != weapon_property.base_range:
                base_range = weapon_property.base_range
                model.base_range = base_range.count if base_range is not None else None
            if old.max_range != weapon_property.max_range:
                max_range = weapon_property.max_range
                model.max_range = max_range.count if max_range is not None else None
            if old.second_hand_dice != weapon_property.second_hand_dice:
                second_hand_dice = weapon_property.second_hand_dice
                model.second_hand_dice_name = (
                    second_hand_dice.dice_type if second_hand_dice is not None else None
                )
                model.second_hand_dice_count = (
                    second_hand_dice.count if second_hand_dice is not None else None
                )
            model.description = weapon_property.description
            await session.commit()

    async def delete(self, weapon_property_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(WeaponPropertyModel).where(
                WeaponPropertyModel.id == weapon_property_id
            )
            result = await session.execute(stmt)
            if result.rowcount == 0:
                raise DomainError.not_found(
                    f"свойства оружия с id {weapon_property_id} не существует"
                )
            await session.commit()
