from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.user import AppUser


class UserRepository(ABC):
    @abstractmethod
    async def id_exists(self, user_id: UUID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self) -> list[AppUser]:
        raise NotImplemented

    @abstractmethod
    async def save(self, user: AppUser) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError()
