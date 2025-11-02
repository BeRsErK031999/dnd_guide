from uuid import UUID

from application.repository.user import UserRepository
from domain.error import DomainError


class UserCheck:
    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository

    def __check_user(self, user_id: UUID) -> None:
        if not self.__user_repository.is_user_of_id_exist(user_id):
            raise DomainError.access("у вас недостаточно прав для совершения операции")
