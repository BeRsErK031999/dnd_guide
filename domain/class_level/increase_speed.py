from domain.length import Length
from domain.mixin import ValueDescription


class ClassLevelIncreaseSpeed(ValueDescription):
    def __init__(
        self,
        speed: Length,
        description: str,
    ) -> None:
        ValueDescription.__init__(self, description)
        self._speed = speed

    def speed(self) -> Length:
        return self._speed

    def __eq__(self, value: object) -> bool:
        if value is None:
            return False
        if isinstance(value, self.__class__):
            return (
                self._speed == value._speed and self._description == value._description
            )
        raise NotImplemented
