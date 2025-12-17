from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import SourceModel
from application.dto.model.source import AppSource
from application.repository import SourceRepository as AppSourceRepository
from domain.source import SourceRepository as DomainSourceRepository
from sqlalchemy import delete, exists, or_, select


class SQLSourceRepository(DomainSourceRepository, AppSourceRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(SourceModel)).where(SourceModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, source_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(SourceModel)).where(SourceModel.id == source_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, source_id: UUID) -> AppSource:
        async with self.__db_helper.session as session:
            query = select(SourceModel).where(SourceModel.id == source_id)
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_app()

    async def filter(self, search_by_name: str | None = None) -> list[AppSource]:
        async with self.__db_helper.session as session:
            query = select(SourceModel)
            if search_by_name:
                query = query.where(
                    or_(
                        SourceModel.name.ilike(f"%{search_by_name}%"),
                        SourceModel.name_in_english.ilike(f"%{search_by_name}%"),
                    )
                )
            result = await session.execute(query)
            result = result.scalars().all()
            return [source.to_app() for source in result]

    async def get_all(self) -> list[AppSource]:
        async with self.__db_helper.session as session:
            query = select(SourceModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [source.to_app() for source in result]

    async def save(self, source: AppSource) -> None:
        async with self.__db_helper.session as session:
            await session.merge(SourceModel.from_app(source))
            await session.commit()

    async def delete(self, source_id: UUID) -> None:
        async with self.__db_helper.session as session:
            query = delete(SourceModel).where(SourceModel.id == source_id)
            await session.execute(query)
            await session.commit()
