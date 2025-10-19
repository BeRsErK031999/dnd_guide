from application.repositories import UserRepository
from domain.user import UserID
from domain.user.user import User


class CreateUserCommand:
    def __init__(self, user_repository: UserRepository) -> None:
        self.__repository = user_repository

    def execute(self, user_id: UserID) -> None:
        if self.__repository.is_user_of_id_exist(user_id=user_id):
            return
        user = User(user_id=user_id)
        self.__repository.user_create(user=user)
