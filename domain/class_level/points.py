from domain.mixin import ValueDescription


class ClassLevelPoints(ValueDescription):
    def __init__(self, points: int, description: str) -> None:
        ValueDescription.__init__(self, description)
        self._points = points

    def points(self) -> int:
        return self._points

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._points == value._points
                and self._description == value._description
            )
        raise NotImplemented
