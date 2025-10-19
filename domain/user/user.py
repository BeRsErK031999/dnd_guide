from domain.user.user_id import UserID


class User:
    def __init__(self, user_id: UserID) -> None:
        self.__user_id = user_id

    def user_id(self) -> UserID:
        return self.__user_id
