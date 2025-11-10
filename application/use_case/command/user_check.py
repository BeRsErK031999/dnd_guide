from uuid import UUID

from application.repository.user import UserRepository
from domain.error import DomainError


class UserCheck:
    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository

    async def _user_check(self, user_id: UUID) -> None:
        if not await self.__user_repository.id_exists(user_id):
            raise DomainError.access("у вас недостаточно прав для совершения операции")
