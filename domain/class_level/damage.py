from domain.mixin import ValueDescription


class ClassLevelBonusDamage(ValueDescription):
    def __init__(self, damage: int, description: str) -> None:
        ValueDescription.__init__(self, description)
        self.__damage = damage

    def damage(self) -> int:
        return self.__damage

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__damage == value.__damage
                and self.__description == value.__description
            )
        raise NotImplemented
