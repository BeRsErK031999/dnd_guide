from application.command.user.repository import UserRepository
from domain.user import UserID
from domain.user.user import User


class RemoveUserCommand:
    def __init__(self, user_repository: UserRepository) -> None:
        self.__repository = user_repository

    def execute(self, user_id: UserID) -> None:
        if not self.__repository.is_user_of_id_exist(user_id=user_id):
            return
        self.__repository.user_remove(user_id=user_id)
