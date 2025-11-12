from uuid import UUID

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import UserModel
from application.repository import UserRepository
from domain.user import User
from sqlalchemy import delete, exists, select


class SQLUserRepository(UserRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def id_exists(self, user_id: UUID) -> bool:
        async with self.__helper.session() as session:
            query = select(exists(UserModel)).where(UserModel.id == user_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_all(self) -> list[User]:
        async with self.__helper.session() as session:
            query = select(UserModel)
            result = await session.execute(query)
            users = result.scalars().all()
            return [user.to_domain_user() for user in users]

    async def create(self, user: User) -> None:
        async with self.__helper.session() as session:
            session.add(UserModel.from_domain_user(user))
            await session.commit()

    async def delete(self, user_id: UUID) -> None:
        async with self.__helper.session() as session:
            stmt = delete(UserModel).where(UserModel.id == user_id)
            await session.execute(stmt)
            await session.commit()
