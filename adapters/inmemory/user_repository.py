from uuid import UUID

from app_error import AppError
from application.repositories import UserRepository
from domain.user import User, UserID


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.__user_store: dict[UUID, User] = dict()

    def is_user_of_id_exist(self, user_id: UserID) -> bool:
        return bool(self.__user_store.get(user_id.user_id(), False))

    def user_create(self, user: User) -> None:
        if self.is_user_of_id_exist(user.user_id()):
            raise AppError.internal(
                f"пользователь с id {user.user_id()} уже существует"
            )
        self.__user_store[user.user_id().user_id()] = user

    def user_remove(self, user_id: UserID) -> None:
        if not self.is_user_of_id_exist(user_id):
            raise AppError.internal(f"пользователь с id {user_id} не существует")
        self.__user_store.pop(user_id.user_id())
