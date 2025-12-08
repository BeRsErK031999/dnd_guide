from domain.mixin import ValueDescription


class RaceAge(ValueDescription):
    def __init__(self, max_age: int, description: str) -> None:
        ValueDescription.__init__(self, description)
        self._max_age = max_age

    def max_age(self) -> int:
        return self._max_age

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._max_age == value._max_age
                and self._description == value._description
            )
        raise NotImplemented
