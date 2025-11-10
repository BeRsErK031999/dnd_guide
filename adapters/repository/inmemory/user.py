from uuid import UUID

from application.repository import UserRepository
from domain.user import User


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, User] = {}

    async def id_exists(self, user_id: UUID) -> bool:
        return user_id in self.__store

    async def get_all(self) -> list[User]:
        return list(self.__store.values())

    async def save(self, user: User) -> None:
        self.__store[user.user_id()] = user

    async def delete(self, user_id: UUID) -> None:
        del self.__store[user_id]
