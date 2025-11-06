from abc import ABC, abstractmethod
from uuid import UUID

from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def is_user_of_id_exist(self, user_id: UUID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError()
