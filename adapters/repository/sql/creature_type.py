from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import CreatureTypeModel
from application.repository import CreatureTypeRepository as AppCreatureTypeRepository
from domain.creature_type import CreatureType
from domain.creature_type import CreatureTypeRepository as DomainCreatureTypeRepository
from sqlalchemy import delete, exists, select


class SQLCreatureTypeRepository(
    DomainCreatureTypeRepository, AppCreatureTypeRepository
):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(CreatureTypeModel)).where(
                CreatureTypeModel.name == name
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, creature_type_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(CreatureTypeModel)).where(
                CreatureTypeModel.id == creature_type_id
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, creature_type_id: UUID) -> CreatureType:
        async with self.__db_helper.session as session:
            query = select(CreatureTypeModel).where(
                CreatureTypeModel.id == creature_type_id
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[CreatureType]:
        async with self.__db_helper.session as session:
            query = select(CreatureTypeModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [r.to_domain() for r in result]

    async def create(self, creature_type: CreatureType) -> None:
        async with self.__db_helper.session as session:
            session.add(CreatureTypeModel.from_domain(creature_type))
            await session.commit()

    async def update(self, creature_type: CreatureType) -> None:
        async with self.__db_helper.session as session:
            await session.merge(CreatureTypeModel.from_domain(creature_type))
            await session.commit()

    async def delete(self, creature_type_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(CreatureTypeModel).where(
                CreatureTypeModel.id == creature_type_id
            )
            await session.execute(stmt)
            await session.commit()
