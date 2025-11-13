from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import CreatureSizeModel
from application.repository import CreatureSizeRepository as AppCreatureSizeRepository
from domain.creature_size import CreatureSize
from domain.creature_size import CreatureSizeRepository as DomainCreatureSizeRepository
from sqlalchemy import delete, exists, select


class SQLCreatureSizeRepository(
    DomainCreatureSizeRepository, AppCreatureSizeRepository
):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(CreatureSizeModel)).where(
                CreatureSizeModel.name == name
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, size_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(CreatureSizeModel)).where(
                CreatureSizeModel.id == size_id
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, size_id: UUID) -> CreatureSize:
        async with self.__db_helper.session as session:
            query = select(CreatureSizeModel).where(CreatureSizeModel.id == size_id)
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[CreatureSize]:
        async with self.__db_helper.session as session:
            query = select(CreatureSizeModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [r.to_domain() for r in result]

    async def create(self, size: CreatureSize) -> None:
        async with self.__db_helper.session as session:
            session.add(CreatureSizeModel.from_domain(size))
            await session.commit()

    async def update(self, size: CreatureSize) -> None:
        async with self.__db_helper.session as session:
            await session.merge(CreatureSizeModel.from_domain(size))
            await session.commit()

    async def delete(self, size_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(CreatureSizeModel).where(CreatureSizeModel.id == size_id)
            await session.execute(stmt)
            await session.commit()
