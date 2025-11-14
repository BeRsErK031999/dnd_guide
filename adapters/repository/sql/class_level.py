from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    CharacterClassModel,
    ClassLevelModel,
    ClassLevelSpellSlotModel,
)
from application.repository import ClassLevelRepository as AppClassLevelRepository
from domain.class_level import ClassLevel
from domain.class_level import ClassLevelRepository as DomainClassLevelRepository
from sqlalchemy import delete, exists, select
from sqlalchemy.orm import selectinload


class InMemoryClassLevelRepository(DomainClassLevelRepository, AppClassLevelRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def level_of_class_exists(self, class_id: UUID, level: int) -> bool:
        async with self.__helper.session as session:
            query = select(exists(ClassLevelModel)).where(
                ClassLevelModel.character_class_id == class_id,
                ClassLevelModel.level == level,
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, level_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(ClassLevelModel)).where(
                ClassLevelModel.id == level_id
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, level_id: UUID) -> ClassLevel:
        async with self.__helper.session as session:
            query = (
                select(ClassLevelModel)
                .where(ClassLevelModel.id == level_id)
                .options(
                    selectinload(
                        ClassLevelModel.class_level_spell_slot,
                        ClassLevelModel.character_class,
                    )
                )
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[ClassLevel]:
        async with self.__helper.session as session:
            query = select(ClassLevelModel).options(
                selectinload(
                    ClassLevelModel.class_level_spell_slot,
                    ClassLevelModel.character_class,
                )
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [level.to_domain() for level in result]

    async def create(self, level: ClassLevel) -> None:
        async with self.__helper.session as session:
            model = ClassLevelModel.from_domain(level)
            spell_slots = level.spell_slots()
            if spell_slots is not None:
                model.class_level_spell_slot = ClassLevelSpellSlotModel.from_domain(
                    level.level_id(), spell_slots
                )
            character_class = await session.get_one(
                CharacterClassModel, level.class_id()
            )
            model.character_class = character_class
            session.add(model)
            await session.commit()

    async def update(self, level: ClassLevel) -> None:
        async with self.__helper.session as session:
            model_query = (
                select(ClassLevelModel)
                .where(ClassLevelModel.id == level.level_id())
                .options(
                    selectinload(
                        ClassLevelModel.class_level_spell_slot,
                        ClassLevelModel.character_class,
                    )
                )
            )
            model = await session.execute(model_query)
            model = model.scalar_one()
            old_domain = model.to_domain()
            if old_domain.class_id() != level.class_id():
                character_class = await session.get_one(
                    CharacterClassModel, level.class_id()
                )
                model.character_class = character_class
            if old_domain.level() != level.level():
                model.level = level.level()
            if old_domain.dice() != level.dice():
                dice = level.dice()
                if dice is not None:
                    model.dice_count = dice.dice().count()
                    model.dice_name = dice.dice().dice_type().name
                    model.dice_description = dice.description()
                else:
                    model.dice_count = None
                    model.dice_name = None
                    model.dice_description = None
            if old_domain.spell_slots() != level.spell_slots():
                spell_slots = level.spell_slots()
                if spell_slots is not None:
                    model.class_level_spell_slot = ClassLevelSpellSlotModel.from_domain(
                        level.level_id(), spell_slots
                    )
                else:
                    model.class_level_spell_slot = None
            if old_domain.number_cantrips_know() != level.number_cantrips_know():
                model.number_cantrips_know = level.number_cantrips_know()
            if old_domain.number_spells_know() != level.number_spells_know():
                model.number_spells_know = level.number_spells_know()
            if old_domain.number_arcanums_know() != level.number_arcanums_know():
                model.number_arcanums_know = level.number_arcanums_know()
            if old_domain.points() != level.points():
                points = level.points()
                if points is not None:
                    model.points = points.points()
                    model.points_description = points.description()
                else:
                    model.points = None
                    model.points_description = None
            if old_domain.bonus_damage() != level.bonus_damage():
                bonus_damage = level.bonus_damage()
                if bonus_damage is not None:
                    model.bonus_damage = bonus_damage.damage()
                    model.bonus_damage_description = bonus_damage.description()
                else:
                    model.bonus_damage = None
                    model.bonus_damage_description = None
            if old_domain.increase_speed() != level.increase_speed():
                increase_speed = level.increase_speed()
                if increase_speed is not None:
                    model.increase_speed = increase_speed.speed().in_ft()
                    model.increase_speed_description = increase_speed.description()
                else:
                    model.increase_speed = None
                    model.increase_speed_description = None
            await session.commit()

    async def delete(self, level_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(ClassLevelModel).where(ClassLevelModel.id == level_id)
            await session.execute(stmt)
            await session.commit()
