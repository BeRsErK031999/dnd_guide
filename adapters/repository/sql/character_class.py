from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    CharacterClassModel,
    ClassArmorTypeModel,
    ClassPrimaryModifierModel,
    ClassSavingThrowModel,
    ClassSkillModel,
    SourceModel,
    ToolModel,
    WeaponModel,
)
from application.dto.model.character_class import AppClass
from application.repository import ClassRepository as AppClassRepository
from domain.character_class import ClassRepository as DomainClassRepository
from sqlalchemy import Select, delete, exists, or_, select
from sqlalchemy.orm import joinedload, selectinload


class SQLClassRepository(DomainClassRepository, AppClassRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists().where(CharacterClassModel.name == name))
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, class_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists().where(CharacterClassModel.id == class_id))
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, class_id: UUID) -> AppClass:
        async with self.__helper.session as session:
            query = self._add_options(
                select(CharacterClassModel).where(CharacterClassModel.id == class_id)
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_app()

    async def get_all(self) -> list[AppClass]:
        async with self.__helper.session as session:
            query = self._add_options(select(CharacterClassModel))
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_source_ids: list[UUID] | None = None,
        filter_by_tool_ids: list[UUID] | None = None,
        filter_by_weapon_ids: list[UUID] | None = None,
    ) -> list[AppClass]:
        async with self.__helper.session as session:
            query = self._add_options(select(CharacterClassModel))
            if search_by_name is not None:
                query = query.where(
                    or_(
                        CharacterClassModel.name.ilike(f"%{search_by_name}%"),
                        CharacterClassModel.name_in_english.ilike(
                            f"%{search_by_name}%"
                        ),
                    )
                )
            if filter_by_source_ids is not None:
                query = query.where(
                    CharacterClassModel.source_id.in_(filter_by_source_ids)
                )
            if filter_by_tool_ids is not None:
                query = query.where(
                    exists().where(
                        CharacterClassModel.tools.any(
                            ToolModel.id.in_(filter_by_tool_ids)
                        )
                    )
                )
            if filter_by_weapon_ids is not None:
                query = query.where(
                    exists().where(
                        CharacterClassModel.weapons.any(
                            WeaponModel.id.in_(filter_by_weapon_ids)
                        )
                    )
                )
            result = await session.execute(query)
            return [item.to_app() for item in result.scalars().all()]

    async def save(self, character_class: AppClass) -> None:
        if await self.id_exists(character_class.class_id):
            await self.update(character_class)
        await self.create(character_class)

    async def create(self, character_class: AppClass) -> None:
        async with self.__helper.session as session:
            model = CharacterClassModel.from_app(character_class)
            prof = character_class.proficiencies
            model.primary_modifiers = [
                ClassPrimaryModifierModel.from_app(character_class.class_id, m)
                for m in character_class.primary_modifiers
            ]
            model.armor_types = [
                ClassArmorTypeModel.from_app(character_class.class_id, t)
                for t in prof.armors
            ]
            model.saving_throws = [
                ClassSavingThrowModel.from_app(character_class.class_id, m)
                for m in prof.saving_throws
            ]
            model.skills = [
                ClassSkillModel.from_app(character_class.class_id, s)
                for s in prof.skills
            ]
            weapons_query = select(WeaponModel).where(WeaponModel.id.in_(prof.weapons))
            weapons = await session.execute(weapons_query)
            weapons = weapons.scalars().all()
            model.weapons.extend(weapons)
            tools_query = select(ToolModel).where(ToolModel.id.in_(prof.tools))
            tools = await session.execute(tools_query)
            tools = tools.scalars().all()
            model.tools.extend(tools)
            model.source = await session.get_one(SourceModel, character_class.source_id)
            session.add(model)
            await session.commit()

    async def update(self, character_class: AppClass) -> None:
        async with self.__helper.session as session:
            model_query = self._add_options(
                select(CharacterClassModel).where(
                    CharacterClassModel.id == character_class.class_id
                )
            )
            model = await session.execute(model_query)
            model = model.scalar_one()
            old = model.to_app()
            if old.name != character_class.name:
                model.name = character_class.name
            if old.name_in_english != character_class.name_in_english:
                model.name_in_english = character_class.name_in_english
            if old.primary_modifiers != character_class.primary_modifiers:
                model.primary_modifiers.clear()
                if len(old.primary_modifiers) > 0:
                    model.primary_modifiers.extend(
                        [
                            ClassPrimaryModifierModel.from_app(
                                character_class.class_id, m
                            )
                            for m in character_class.primary_modifiers
                        ]
                    )
            if old.hits != character_class.hits:
                hits = character_class.hits
                model.hit_dice_name = hits.hit_dice.dice_type
                model.hit_dice_count = hits.hit_dice.count
                model.starting_hits = hits.starting_hits
                model.hit_modifier = hits.hit_modifier
                model.next_level_hits = hits.next_level_hits
            if old.proficiencies != character_class.proficiencies:
                prof = character_class.proficiencies
                model.number_skills = prof.number_skills
                model.number_tools = prof.number_tools
                model.armor_types.clear()
                if len(prof.armors) > 0:
                    model.armor_types.extend(
                        [
                            ClassArmorTypeModel.from_app(character_class.class_id, a)
                            for a in prof.armors
                        ]
                    )
                model.saving_throws.clear()
                if len(prof.saving_throws) > 0:
                    model.saving_throws.extend(
                        [
                            ClassSavingThrowModel.from_app(character_class.class_id, m)
                            for m in prof.saving_throws
                        ]
                    )
                model.skills.clear()
                if len(prof.skills) > 0:
                    model.skills.extend(
                        [
                            ClassSkillModel.from_app(character_class.class_id, s)
                            for s in prof.skills
                        ]
                    )
                model.weapons.clear()
                if len(prof.weapons) > 0:
                    weapons_query = select(WeaponModel).where(
                        WeaponModel.id.in_(prof.weapons)
                    )
                    weapons = await session.execute(weapons_query)
                    weapons = weapons.scalars().all()
                    model.weapons.extend(weapons)
                model.tools.clear()
                if len(prof.tools) > 0:
                    tools_query = select(ToolModel).where(ToolModel.id.in_(prof.tools))
                    tools = await session.execute(tools_query)
                    tools = tools.scalars().all()
                    model.tools.extend(tools)
            if old.source_id != character_class.source_id:
                model.source = await session.get_one(
                    SourceModel, character_class.source_id
                )
            model.description = character_class.description

    async def delete(self, class_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(CharacterClassModel).where(CharacterClassModel.id == class_id)
            await session.execute(stmt)
            await session.commit()

    def _add_options(
        self, query: Select[tuple[CharacterClassModel]]
    ) -> Select[tuple[CharacterClassModel]]:
        return query.options(
            selectinload(CharacterClassModel.primary_modifiers),
            selectinload(CharacterClassModel.armor_types),
            selectinload(CharacterClassModel.saving_throws),
            selectinload(CharacterClassModel.skills),
            selectinload(CharacterClassModel.weapons),
            selectinload(CharacterClassModel.tools),
            joinedload(CharacterClassModel.source),
        )
