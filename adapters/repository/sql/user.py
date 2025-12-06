from uuid import UUID

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import UserModel
from application.dto.model.user import AppUser
from application.repository import UserRepository
from sqlalchemy import delete, exists, select


class SQLUserRepository(UserRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def id_exists(self, user_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(UserModel)).where(UserModel.id == user_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_all(self) -> list[AppUser]:
        async with self.__helper.session as session:
            query = select(UserModel)
            result = await session.execute(query)
            users = result.scalars().all()
            return [user.to_app() for user in users]

    async def create(self, user: AppUser) -> None:
        async with self.__helper.session as session:
            session.add(UserModel.from_app(user))
            await session.commit()

    async def delete(self, user_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(UserModel).where(UserModel.id == user_id)
            await session.execute(stmt)
            await session.commit()
