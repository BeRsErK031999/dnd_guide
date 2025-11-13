from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import ArmorModel, MaterialModel
from application.repository import ArmorRepository as AppArmorRepository
from domain.armor import Armor
from domain.armor import ArmorRepository as DomainArmorRepository
from sqlalchemy import delete, exists, select


class SQLArmorRepository(DomainArmorRepository, AppArmorRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists(ArmorModel)).where(ArmorModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, armor_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(ArmorModel)).where(ArmorModel.id == armor_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, armor_id: UUID) -> Armor:
        async with self.__helper.session as session:
            query = select(ArmorModel).where(ArmorModel.id == armor_id)
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[Armor]:
        async with self.__helper.session as session:
            query = select(ArmorModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [armor.to_domain() for armor in result]

    async def create(self, armor: Armor) -> None:
        async with self.__helper.session as session:
            model = ArmorModel.from_domain(armor)
            model.material = await session.get_one(MaterialModel, armor.material_id())
            session.add(model)
            await session.commit()

    async def update(self, armor: Armor) -> None:
        async with self.__helper.session as session:
            query = select(ArmorModel).where(ArmorModel.id == armor.armor_id())
            result = await session.execute(query)
            model = result.scalar_one()
            old_domain = model.to_domain()
            if old_domain.armor_type() != armor.armor_type():
                model.armor_type = armor.armor_type().name
            if old_domain.armor_class() != armor.armor_class():
                model.base_class = armor.armor_class().base_class()
                modifier = armor.armor_class().modifier()
                model.modifier = modifier.name if modifier is not None else None
                max_modifier_bonus = armor.armor_class().max_modifier_bonus()
                model.max_modifier_bonus = (
                    max_modifier_bonus if max_modifier_bonus is not None else None
                )
            if old_domain.strength() != armor.strength():
                model.strength = armor.strength()
            if old_domain.stealth() != armor.stealth():
                model.stealth = armor.stealth()
            if old_domain.weight() != armor.weight():
                model.weight = armor.weight().in_lb()
            if old_domain.cost() != armor.cost():
                model.cost = armor.cost().in_copper()
            if old_domain.material_id() != armor.material_id():
                model.material = await session.get_one(
                    MaterialModel, armor.material_id()
                )
            await session.commit()

    async def delete(self, armor_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(ArmorModel).where(ArmorModel.id == armor_id)
            await session.execute(stmt)
            await session.commit()
