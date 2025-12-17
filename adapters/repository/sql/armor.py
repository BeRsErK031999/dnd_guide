from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import ArmorModel, MaterialModel
from application.dto.model.armor import AppArmor
from application.repository import ArmorRepository as AppArmorRepository
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

    async def get_by_id(self, armor_id: UUID) -> AppArmor:
        async with self.__helper.session as session:
            query = select(ArmorModel).where(ArmorModel.id == armor_id)
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_app()

    async def get_all(self) -> list[AppArmor]:
        async with self.__helper.session as session:
            query = select(ArmorModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [armor.to_app() for armor in result]

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_armor_types: list[str] | None = None,
        filter_by_material_ids: list[UUID] | None = None,
    ) -> list[AppArmor]:
        async with self.__helper.session as session:
            query = select(ArmorModel)
            conditions = list()
            if search_by_name is not None:
                conditions.append(ArmorModel.name.ilike(f"%{search_by_name}%"))
            if filter_by_armor_types is not None:
                conditions.append(ArmorModel.armor_type.in_(filter_by_armor_types))
            if filter_by_material_ids is not None:
                conditions.append(ArmorModel.material_id.in_(filter_by_material_ids))
            if len(conditions) > 0:
                query = query.where(*conditions)
            result = await session.execute(query)
            return [armor.to_app() for armor in result.scalars().all()]

    async def save(self, armor: AppArmor) -> None:
        if await self.id_exists(armor.armor_id):
            await self.update(armor)
        await self.create(armor)

    async def create(self, armor: AppArmor) -> None:
        async with self.__helper.session as session:
            model = ArmorModel.from_app(armor)
            model.material = await session.get_one(MaterialModel, armor.material_id)
            session.add(model)
            await session.commit()

    async def update(self, armor: AppArmor) -> None:
        async with self.__helper.session as session:
            query = select(ArmorModel).where(ArmorModel.id == armor.armor_id)
            result = await session.execute(query)
            model = result.scalar_one()
            old = model.to_app()
            if old.armor_type != armor.armor_type:
                model.armor_type = armor.armor_type
            if old.armor_class != armor.armor_class:
                model.base_class = armor.armor_class.base_class
                model.modifier = armor.armor_class.modifier
                max_modifier_bonus = armor.armor_class.max_modifier_bonus
                model.max_modifier_bonus = max_modifier_bonus
            if old.strength != armor.strength:
                model.strength = armor.strength
            if old.stealth != armor.stealth:
                model.stealth = armor.stealth
            if old.weight != armor.weight:
                model.weight = armor.weight.count
            if old.cost != armor.cost:
                model.cost = armor.cost.count
            if old.material_id != armor.material_id:
                model.material = await session.get_one(MaterialModel, armor.material_id)
            await session.commit()

    async def delete(self, armor_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(ArmorModel).where(ArmorModel.id == armor_id)
            await session.execute(stmt)
            await session.commit()
