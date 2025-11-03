from domain.length import Length
from domain.mixin import ValueDescription


class ClassLevelIncreaseSpeed(ValueDescription):
    def __init__(
        self,
        speed: Length,
        description: str,
    ) -> None:
        ValueDescription.__init__(self, description)
        self.__speed = speed

    def speed(self) -> Length:
        return self.__speed

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__speed == value.__speed
                and self.__description == value.__description
            )
        raise NotImplemented
