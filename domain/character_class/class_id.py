from uuid import UUID


class ClassID:
    def __init__(self, character_id: UUID) -> None:
        self.__character_id = character_id

    def character_id(self) -> UUID:
        return self.__character_id

    def __str__(self) -> str:
        return self.__character_id.__str__()
