from abc import ABC

from application.command.character_class.repository import ClassRepository
from application.command.user import UserRepository
from domain.error import DomainError
from domain.user.user_id import UserID


class BaseCommand(ABC):
    def __init__(
        self, user_repository: UserRepository, class_repository: ClassRepository
    ) -> None:
        self.__user_repository = user_repository
        self.__class_repository = class_repository

    def assert_access(self, user_id: UserID) -> None:
        if not self.__user_repository.is_user_of_id_exist(user_id):
            raise DomainError.access("")
