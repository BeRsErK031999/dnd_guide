from uuid import UUID


class User:
    def __init__(self, user_id: UUID) -> None:
        self._user_id = user_id

    def user_id(self) -> UUID:
        return self._user_id

    def __str__(self) -> str:
        return self._user_id.__str__()

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._user_id == value._user_id
        if isinstance(value, UUID):
            return self._user_id == value
        raise NotImplemented
