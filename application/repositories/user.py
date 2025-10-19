from abc import ABC, abstractmethod

from domain.user import User, UserID


class UserRepository(ABC):
    @abstractmethod
    def is_user_of_id_exist(self, user_id: UserID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def user_create(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    def user_remove(self, user_id: UserID) -> None:
        raise NotImplementedError()
