from abc import ABC, abstractmethod
from uuid import UUID

from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def id_exists(self, user_id: UUID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self) -> list[User]:
        raise NotImplemented

    @abstractmethod
    async def create(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError()
