from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import CharacterClassModel, CharacterSubclassModel
from application.dto.model.character_subclass import AppSubclass
from application.repository import SubclassRepository as AppSubclassRepository
from domain.character_subclass import SubclassRepository as DomainSubclassRepository
from sqlalchemy import delete, exists, select
from sqlalchemy.orm import selectinload


class SQLSubclassRepository(DomainSubclassRepository, AppSubclassRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists().where(CharacterSubclassModel.name == name))
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, subclass_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists().where(CharacterSubclassModel.id == subclass_id))
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, subclass_id: UUID) -> AppSubclass:
        async with self.__helper.session as session:
            query = (
                select(CharacterSubclassModel)
                .where(CharacterSubclassModel.id == subclass_id)
                .options(selectinload(CharacterSubclassModel.character_class))
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_app()

    async def get_all(self) -> list[AppSubclass]:
        async with self.__helper.session as session:
            query = select(CharacterSubclassModel).options(
                selectinload(CharacterSubclassModel.character_class)
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [subclass.to_app() for subclass in result]

    async def filter(self, filter_by_class_id: UUID | None = None) -> list[AppSubclass]:
        async with self.__helper.session as session:
            query = select(CharacterSubclassModel).options(
                selectinload(CharacterSubclassModel.character_class)
            )
            if filter_by_class_id is not None:
                query = query.where(
                    CharacterSubclassModel.character_class_id == filter_by_class_id
                )
            result = await session.execute(query)
            result = result.scalars().all()
            return [subclass.to_app() for subclass in result]

    async def save(self, subclass: AppSubclass) -> None:
        if await self.id_exists(subclass.subclass_id):
            await self.update(subclass)
        else:
            await self.create(subclass)

    async def create(self, subclass: AppSubclass) -> None:
        async with self.__helper.session as session:
            model = CharacterSubclassModel.from_app(subclass)
            model.character_class = await session.get_one(
                CharacterClassModel, subclass.class_id
            )
            session.add(model)
            await session.commit()

    async def update(self, subclass: AppSubclass) -> None:
        async with self.__helper.session as session:
            model_query = select(CharacterSubclassModel).where(
                CharacterSubclassModel.id == subclass.subclass_id
            )
            model = await session.execute(model_query)
            model = model.scalar_one()
            old = model.to_app()
            if old.name != subclass.name:
                model.name = subclass.name
            if old.name_in_english != subclass.name_in_english:
                model.name_in_english = subclass.name_in_english
            if old.class_id != subclass.class_id:
                model.character_class = await session.get_one(
                    CharacterClassModel, subclass.class_id
                )
            model.description = subclass.description
            await session.commit()

    async def delete(self, subclass_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(CharacterSubclassModel).where(
                CharacterSubclassModel.id == subclass_id
            )
            await session.execute(stmt)
            await session.commit()
