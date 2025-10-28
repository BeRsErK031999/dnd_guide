from uuid import UUID


class User:
    def __init__(self, user_id: UUID) -> None:
        self.__user_id = user_id

    def user_id(self) -> UUID:
        return self.__user_id

    def __str__(self) -> str:
        return self.__user_id.__str__()

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__user_id == value.__user_id
        if isinstance(value, UUID):
            return self.__user_id == value
        raise NotImplemented
