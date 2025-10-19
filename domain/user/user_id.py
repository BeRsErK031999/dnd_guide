from uuid import UUID


class UserID:
    def __init__(self, user_id: UUID) -> None:
        self.__user_id = user_id

    def user_id(self) -> UUID:
        return self.__user_id

    def __str__(self) -> str:
        return self.__user_id.__str__()
