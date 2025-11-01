from domain.mixin import ValueDescription


class RaceAge(ValueDescription):
    def __init__(self, max_age: int, description: str) -> None:
        ValueDescription.__init__(self, description)
        self.__max_age = max_age

    def max_age(self) -> int:
        return self.__max_age

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__max_age == value.__max_age
                and self.__description == value.__description
            )
        raise NotImplemented
