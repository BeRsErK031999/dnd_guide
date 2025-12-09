from uuid import UUID

from application.dto.model.user import AppUser
from application.repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppUser] = {}

    async def id_exists(self, user_id: UUID) -> bool:
        return user_id in self._store

    async def get_all(self) -> list[AppUser]:
        return list(self._store.values())

    async def create(self, user: AppUser) -> None:
        self._store[user.user_id] = user

    async def delete(self, user_id: UUID) -> None:
        del self._store[user_id]
