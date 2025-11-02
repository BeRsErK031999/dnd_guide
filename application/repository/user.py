from abc import ABC, abstractmethod
from uuid import UUID

from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def is_user_of_id_exist(self, user_id: UUID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def create(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        raise NotImplementedError()
