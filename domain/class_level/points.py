from domain.mixin import ValueDescription


class ClassLevelPoints(ValueDescription):
    def __init__(self, points: int, points_description: str) -> None:
        ValueDescription.__init__(self, points_description)
        self.__points = points

    def points(self) -> int:
        return self.__points

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__points == value.__points
                and self.__description == value.__description
            )
        raise NotImplemented
