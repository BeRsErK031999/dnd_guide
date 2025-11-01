from domain.length import Length
from domain.mixin import ValueDescription


class RaceSpeed(ValueDescription):
    def __init__(self, base_speed: Length, description: str) -> None:
        ValueDescription.__init__(self, description)
        self.__base_speed = base_speed

    def base_speed(self) -> Length:
        return self.__base_speed

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__base_speed == value.__base_speed
                and self.__description == value.__description
            )
        raise NotImplemented
