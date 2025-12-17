from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    CharacterClassModel,
    ClassLevelModel,
    ClassLevelSpellSlotModel,
)
from application.dto.model.class_level import AppClassLevel
from application.repository import ClassLevelRepository as AppClassLevelRepository
from domain.class_level import ClassLevelRepository as DomainClassLevelRepository
from domain.error import DomainError
from sqlalchemy import Select, delete, exists, select
from sqlalchemy.orm import joinedload


class SQLClassLevelRepository(DomainClassLevelRepository, AppClassLevelRepository):
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

    async def get_by_id(self, level_id: UUID) -> AppClassLevel:
        async with self.__helper.session as session:
            query = self._add_options(
                select(ClassLevelModel).where(ClassLevelModel.id == level_id)
            )
            result = await session.execute(query)
            result = result.scalar()
            if result is None:
                raise DomainError.not_found(f"уровень с id {level_id} не существует")
            return result.to_app()

    async def get_all(self) -> list[AppClassLevel]:
        async with self.__helper.session as session:
            query = self._add_options(select(ClassLevelModel))
            result = await session.execute(query)
            result = result.scalars().all()
            return [level.to_app() for level in result]

    async def filter(
        self, filter_by_class_id: UUID | None = None
    ) -> list[AppClassLevel]:
        async with self.__helper.session as session:
            query = select(ClassLevelModel)
            if filter_by_class_id is not None:
                query = query.where(
                    ClassLevelModel.character_class_id == filter_by_class_id
                )
            query = self._add_options(query)
            result = await session.execute(query)
            result = result.scalars().all()
            return [level.to_app() for level in result]

    async def save(self, level: AppClassLevel) -> None:
        if await self.id_exists(level.class_level_id):
            await self.update(level)
        else:
            await self.create(level)

    async def create(self, level: AppClassLevel) -> None:
        async with self.__helper.session as session:
            model = ClassLevelModel.from_app(level)
            spell_slots = level.spell_slots
            if spell_slots is not None:
                model.class_level_spell_slot = ClassLevelSpellSlotModel.from_app(
                    level.class_level_id, spell_slots
                )
            character_class = await session.get_one(CharacterClassModel, level.class_id)
            model.character_class = character_class
            session.add(model)
            await session.commit()

    async def update(self, level: AppClassLevel) -> None:
        async with self.__helper.session as session:
            model_query = self._add_options(
                select(ClassLevelModel).where(
                    ClassLevelModel.id == level.class_level_id
                )
            )
            model = await session.execute(model_query)
            model = model.scalar_one()
            old = model.to_app()
            if old.class_id != level.class_id:
                character_class = await session.get_one(
                    CharacterClassModel, level.class_id
                )
                model.character_class = character_class
            if old.level != level.level:
                model.level = level.level
            if old.dice != level.dice:
                dice = level.dice
                if dice is not None:
                    model.dice_count = dice.dice.count
                    model.dice_name = dice.dice.dice_type
                    model.dice_description = dice.description
                else:
                    model.dice_count = None
                    model.dice_name = None
                    model.dice_description = None
            if old.spell_slots != level.spell_slots:
                spell_slots = level.spell_slots
                if spell_slots is not None:
                    model.class_level_spell_slot = ClassLevelSpellSlotModel.from_app(
                        level.class_level_id, spell_slots
                    )
                else:
                    model.class_level_spell_slot = None
            if old.number_cantrips_know != level.number_cantrips_know:
                model.number_cantrips_know = level.number_cantrips_know
            if old.number_spells_know != level.number_spells_know:
                model.number_spells_know = level.number_spells_know
            if old.number_arcanums_know != level.number_arcanums_know:
                model.number_arcanums_know = level.number_arcanums_know
            if old.points != level.points:
                points = level.points
                if points is not None:
                    model.points = points.points
                    model.points_description = points.description
                else:
                    model.points = None
                    model.points_description = None
            if old.bonus_damage != level.bonus_damage:
                bonus_damage = level.bonus_damage
                if bonus_damage is not None:
                    model.bonus_damage = bonus_damage.damage
                    model.bonus_damage_description = bonus_damage.description
                else:
                    model.bonus_damage = None
                    model.bonus_damage_description = None
            if old.increase_speed != level.increase_speed:
                increase_speed = level.increase_speed
                if increase_speed is not None:
                    model.increase_speed = increase_speed.speed.count
                    model.increase_speed_description = increase_speed.description
                else:
                    model.increase_speed = None
                    model.increase_speed_description = None
            await session.commit()

    async def delete(self, level_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(ClassLevelModel).where(ClassLevelModel.id == level_id)
            result = await session.execute(stmt)
            if result.rowcount == 0:
                raise DomainError.not_found(f"уровень с id {level_id} не существует")
            await session.commit()

    def _add_options(
        self, query: Select[tuple[ClassLevelModel]]
    ) -> Select[tuple[ClassLevelModel]]:
        return query.options(
            joinedload(ClassLevelModel.class_level_spell_slot),
            joinedload(ClassLevelModel.character_class),
        )
