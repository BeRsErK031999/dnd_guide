from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import (
    CharacterClassModel,
    CharacterSubclassModel,
    MaterialComponentModel,
    SourceModel,
    SpellModel,
    SpellSavingThrowModel,
)
from application.dto.model.spell import AppSpell
from application.repository import SpellRepository as AppSpellRepository
from domain.spell import SpellRepository as DomainSpellRepository
from sqlalchemy import Select, delete, exists, or_, select
from sqlalchemy.orm import selectinload


class SQLSpellRepository(DomainSpellRepository, AppSpellRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(SpellModel)).where(SpellModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, spell_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(SpellModel)).where(SpellModel.id == spell_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, spell_id: UUID) -> AppSpell:
        async with self.__db_helper.session as session:
            query = self._add_options(
                select(SpellModel).where(SpellModel.id == spell_id)
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_app()

    async def get_all(self) -> list[AppSpell]:
        async with self.__db_helper.session as session:
            query = self._add_options(select(SpellModel))
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_class_ids: list[UUID] | None = None,
        filter_by_subclass_ids: list[UUID] | None = None,
        filter_by_schools: list[str] | None = None,
        filter_by_damage_types: list[str] | None = None,
        filter_by_durations: list[str] | None = None,
        filter_by_casting_times: list[str] | None = None,
        filter_by_verbal_component: bool | None = None,
        filter_by_symbolic_component: bool | None = None,
        filter_by_material_component: bool | None = None,
        filter_by_material_ids: list[UUID] | None = None,
        filter_by_concentration: bool | None = None,
        filter_by_ritual: bool | None = None,
        filter_by_source_ids: list[UUID] | None = None,
    ) -> list[AppSpell]:
        async with self.__db_helper.session as session:
            query = self._add_options(select(SpellModel))
            conditions = list()
            if search_by_name is not None:
                conditions.append(
                    or_(
                        SpellModel.name.ilike(f"%{search_by_name}%"),
                        SpellModel.name_in_english.ilike(f"%{search_by_name}%"),
                    )
                )
            if filter_by_class_ids is not None:
                conditions.append(
                    SpellModel.character_classes.any(
                        CharacterClassModel.id.in_(filter_by_class_ids)
                    )
                )
            if filter_by_subclass_ids is not None:
                conditions.append(
                    SpellModel.character_subclasses.any(
                        CharacterSubclassModel.id.in_(filter_by_subclass_ids)
                    )
                )
            if filter_by_schools is not None:
                conditions.append(SpellModel.school.in_(filter_by_schools))
            if filter_by_damage_types is not None:
                conditions.append(SpellModel.damage_type.in_(filter_by_damage_types))
            if filter_by_durations is not None:
                conditions.append(SpellModel.duration_unit.in_(filter_by_durations))
            if filter_by_casting_times is not None:
                conditions.append(
                    SpellModel.casting_time_unit.in_(filter_by_casting_times)
                )
            if filter_by_verbal_component is not None:
                conditions.append(
                    SpellModel.verbal_component == filter_by_verbal_component
                )
            if filter_by_symbolic_component is not None:
                conditions.append(
                    SpellModel.symbolic_component == filter_by_symbolic_component
                )
            if filter_by_material_component is not None:
                conditions.append(
                    SpellModel.material_component == filter_by_material_component
                )
            if filter_by_material_ids is not None:
                conditions.append(
                    SpellModel.materials.any(
                        MaterialComponentModel.id.in_(filter_by_material_ids)
                    )
                )
            if filter_by_concentration is not None:
                conditions.append(SpellModel.concentration == filter_by_concentration)
            if filter_by_ritual:
                conditions.append(SpellModel.ritual == filter_by_ritual)
            if filter_by_source_ids is not None:
                conditions.append(SpellModel.source_id.in_(filter_by_source_ids))
            if len(conditions) > 0:
                query = query.where(*conditions)
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def save(self, spell: AppSpell) -> None:
        if await self.id_exists(spell.spell_id):
            await self.update(spell)
        else:
            await self.create(spell)

    async def create(self, spell: AppSpell) -> None:
        async with self.__db_helper.session as session:
            model = SpellModel.from_app(spell)
            session.add(model)
            await session.flush()
            if len(spell.class_ids) > 0:
                classes_query = select(CharacterClassModel).where(
                    CharacterClassModel.id.in_(spell.class_ids)
                )
                classes = await session.execute(classes_query)
                classes = classes.scalars().all()
                model.character_classes.extend(classes)
            if len(spell.subclass_ids) > 0:
                subclasses_query = select(CharacterSubclassModel).where(
                    CharacterSubclassModel.id.in_(spell.subclass_ids)
                )
                subclasses = await session.execute(subclasses_query)
                subclasses = subclasses.scalars().all()
                model.character_subclasses.extend(subclasses)
            if len(spell.components.materials) > 0:
                materials_query = select(MaterialComponentModel).where(
                    MaterialComponentModel.id.in_(spell.components.materials)
                )
                materials = await session.execute(materials_query)
                materials = materials.scalars().all()
                model.materials.extend(materials)
            if len(spell.saving_throws) > 0:
                saving_throws = spell.saving_throws
                model.saving_throws.extend(
                    [
                        SpellSavingThrowModel.from_app(model.id, item)
                        for item in saving_throws
                    ]
                )
            session.add(model)
            await session.commit()

    async def update(self, spell: AppSpell) -> None:
        async with self.__db_helper.session as session:
            model_query = self._add_options(
                select(SpellModel).where(SpellModel.id == spell.spell_id)
            )
            model = await session.execute(model_query)
            model = model.scalar_one()
            old_domain = model.to_app()
            if old_domain.name != spell.name:
                model.name = spell.name
            if old_domain.school != spell.school:
                model.school = spell.school
            if old_domain.damage_type != spell.damage_type:
                damage_type = spell.damage_type
                model.damage_type = damage_type if damage_type else None
            if old_domain.duration != spell.duration:
                duration = spell.duration
                model.duration_count = duration.count if duration is not None else None
                model.duration_unit = duration.unit if duration is not None else None
            if old_domain.casting_time != spell.casting_time:
                casting_time = spell.casting_time
                model.casting_time_count = casting_time.count
                model.casting_time_unit = casting_time.unit
            if old_domain.spell_range != spell.spell_range:
                model.spell_range = spell.spell_range.count
            if old_domain.splash != spell.splash:
                splash = spell.splash
                model.splash = splash.count if splash is not None else None
            if old_domain.components != spell.components:
                components = spell.components
                model.symbolic_component = components.symbolic
                model.material_component = components.material
                model.verbal_component = components.verbal
                model.materials.clear()
                if len(components.materials) > 0:
                    materials_query = select(MaterialComponentModel).where(
                        MaterialComponentModel.id.in_(components.materials)
                    )
                    materials = await session.execute(materials_query)
                    materials = materials.scalars().all()
                    model.materials.extend(materials)
            if old_domain.concentration != spell.concentration:
                model.concentration = spell.concentration
            if old_domain.ritual != spell.ritual:
                model.ritual = spell.ritual
            if old_domain.name_in_english != spell.name_in_english:
                model.name_in_english = spell.name_in_english
            if old_domain.source_id != spell.source_id:
                source = await session.get_one(SourceModel, spell.source_id)
                model.source = source
            model.description = spell.description
            model.next_level_description = spell.next_level_description
            model.character_classes.clear()
            if len(spell.class_ids) > 0:
                classes_query = select(CharacterClassModel).where(
                    CharacterClassModel.id.in_(spell.class_ids)
                )
                classes = await session.execute(classes_query)
                classes = classes.scalars().all()
                model.character_classes.extend(classes)
            model.character_subclasses.clear()
            if len(spell.subclass_ids) > 0:
                subclasses_query = select(CharacterSubclassModel).where(
                    CharacterSubclassModel.id.in_(spell.subclass_ids)
                )
                subclasses = await session.execute(subclasses_query)
                subclasses = subclasses.scalars().all()
                model.character_subclasses.extend(subclasses)
            model.saving_throws.clear()
            if len(spell.saving_throws) > 0:
                model.saving_throws.extend(
                    [
                        SpellSavingThrowModel.from_app(model.id, item)
                        for item in spell.saving_throws
                    ]
                )
            await session.commit()

    async def delete(self, spell_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(SpellModel).where(SpellModel.id == spell_id)
            await session.execute(stmt)
            await session.commit()

    def _add_options(
        self, query: Select[tuple[SpellModel]]
    ) -> Select[tuple[SpellModel]]:
        return query.options(
            selectinload(SpellModel.saving_throws),
            selectinload(SpellModel.character_classes),
            selectinload(SpellModel.character_subclasses),
            selectinload(SpellModel.materials),
        )
