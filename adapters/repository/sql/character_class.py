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
from application.repository import ClassRepository as AppClassRepository
from domain.character_class import CharacterClass
from domain.character_class import ClassRepository as DomainClassRepository
from sqlalchemy import delete, exists, select
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

    async def get_by_id(self, class_id: UUID) -> CharacterClass:
        async with self.__helper.session as session:
            query = (
                select(CharacterClassModel)
                .where(CharacterClassModel.id == class_id)
                .options(
                    selectinload(CharacterClassModel.primary_modifiers),
                    selectinload(CharacterClassModel.armor_types),
                    selectinload(CharacterClassModel.saving_throws),
                    selectinload(CharacterClassModel.skills),
                    selectinload(CharacterClassModel.weapons),
                    selectinload(CharacterClassModel.tools),
                    joinedload(CharacterClassModel.source),
                )
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[CharacterClass]:
        async with self.__helper.session as session:
            query = select(CharacterClassModel).options(
                selectinload(CharacterClassModel.primary_modifiers),
                selectinload(CharacterClassModel.armor_types),
                selectinload(CharacterClassModel.saving_throws),
                selectinload(CharacterClassModel.skills),
                selectinload(CharacterClassModel.weapons),
                selectinload(CharacterClassModel.tools),
                joinedload(CharacterClassModel.source),
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_domain() for item in result]

    async def create(self, character_class: CharacterClass) -> None:
        async with self.__helper.session as session:
            model = CharacterClassModel.from_domain(character_class)
            prof = character_class.proficiency()
            model.primary_modifiers = [
                ClassPrimaryModifierModel.from_domain(
                    class_id=character_class.class_id(), modifier=modifier
                )
                for modifier in character_class.primary_modifiers()
            ]
            model.armor_types = [
                ClassArmorTypeModel.from_domain(
                    class_id=character_class.class_id(), armor_type=armor_type
                )
                for armor_type in prof.armors()
            ]
            model.saving_throws = [
                ClassSavingThrowModel.from_domain(
                    class_id=character_class.class_id(), modifier=modifier
                )
                for modifier in prof.saving_throws()
            ]
            model.skills = [
                ClassSkillModel.from_domain(
                    class_id=character_class.class_id(), skill=skill
                )
                for skill in prof.skills()
            ]
            weapons_query = select(WeaponModel).where(
                WeaponModel.id.in_(prof.weapons())
            )
            weapons = await session.execute(weapons_query)
            weapons = weapons.scalars().all()
            model.weapons.extend(weapons)
            tools_query = select(ToolModel).where(ToolModel.id.in_(prof.tools()))
            tools = await session.execute(tools_query)
            tools = tools.scalars().all()
            model.tools.extend(tools)
            model.source = await session.get_one(
                SourceModel, character_class.source_id()
            )
            session.add(model)
            await session.commit()

    async def update(self, character_class: CharacterClass) -> None:
        async with self.__helper.session as session:
            model_query = (
                select(CharacterClassModel)
                .where(CharacterClassModel.id == character_class.class_id())
                .options(
                    selectinload(CharacterClassModel.primary_modifiers),
                    selectinload(CharacterClassModel.armor_types),
                    selectinload(CharacterClassModel.saving_throws),
                    selectinload(CharacterClassModel.skills),
                    selectinload(CharacterClassModel.weapons),
                    selectinload(CharacterClassModel.tools),
                    joinedload(CharacterClassModel.source),
                )
            )
            model = await session.execute(model_query)
            model = model.scalar_one()
            old_domain = model.to_domain()
            if old_domain.name() != character_class.name():
                model.name = character_class.name()
            if old_domain.name_in_english() != character_class.name_in_english():
                model.name_in_english = character_class.name_in_english()
            if old_domain.primary_modifiers() != character_class.primary_modifiers():
                model.primary_modifiers.clear()
                if len(old_domain.primary_modifiers()) > 0:
                    model.primary_modifiers.extend(
                        [
                            ClassPrimaryModifierModel.from_domain(
                                class_id=character_class.class_id(), modifier=modifier
                            )
                            for modifier in character_class.primary_modifiers()
                        ]
                    )
            if old_domain.hits() != character_class.hits():
                hits = character_class.hits()
                model.hit_dice_name = hits.dice().dice_type().name
                model.hit_dice_count = hits.dice().count()
                model.starting_hits = hits.starting()
                model.hit_modifier = hits.modifier().name
                model.next_level_hits = hits.standard_next_level()
            if old_domain.proficiency() != character_class.proficiency():
                prof = character_class.proficiency()
                model.number_skills = prof.number_skills()
                model.number_tools = prof.number_tools()
                model.armor_types.clear()
                if len(prof.armors()) > 0:
                    model.armor_types.extend(
                        [
                            ClassArmorTypeModel.from_domain(
                                class_id=character_class.class_id(),
                                armor_type=armor_type,
                            )
                            for armor_type in prof.armors()
                        ]
                    )
                model.saving_throws.clear()
                if len(prof.saving_throws()) > 0:
                    model.saving_throws.extend(
                        [
                            ClassSavingThrowModel.from_domain(
                                class_id=character_class.class_id(),
                                modifier=modifier,
                            )
                            for modifier in prof.saving_throws()
                        ]
                    )
                model.skills.clear()
                if len(prof.skills()) > 0:
                    model.skills.extend(
                        [
                            ClassSkillModel.from_domain(
                                class_id=character_class.class_id(), skill=skill
                            )
                            for skill in prof.skills()
                        ]
                    )
                model.weapons.clear()
                if len(prof.weapons()) > 0:
                    weapons_query = select(WeaponModel).where(
                        WeaponModel.id.in_(prof.weapons())
                    )
                    weapons = await session.execute(weapons_query)
                    weapons = weapons.scalars().all()
                    model.weapons.extend(weapons)
                model.tools.clear()
                if len(prof.tools()) > 0:
                    tools_query = select(ToolModel).where(
                        ToolModel.id.in_(prof.tools())
                    )
                    tools = await session.execute(tools_query)
                    tools = tools.scalars().all()
                    model.tools.extend(tools)
            if old_domain.source_id() != character_class.source_id():
                model.source = await session.get_one(
                    SourceModel, character_class.source_id()
                )
            model.description = character_class.description()

    async def delete(self, class_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(CharacterClassModel).where(CharacterClassModel.id == class_id)
            await session.execute(stmt)
            await session.commit()
