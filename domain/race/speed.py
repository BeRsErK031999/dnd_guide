from domain.length import Length
from domain.mixin import ValueDescription


class RaceSpeed(ValueDescription):
    def __init__(self, base_speed: Length, description: str) -> None:
        ValueDescription.__init__(self, description)
        self._base_speed = base_speed

    def base_speed(self) -> Length:
        return self._base_speed

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._base_speed == value._base_speed
                and self._description == value._description
            )
        raise NotImplemented
