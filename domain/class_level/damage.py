from domain.mixin import ValueDescription


class ClassLevelBonusDamage(ValueDescription):
    def __init__(self, damage: int, description: str) -> None:
        ValueDescription.__init__(self, description)
        self._damage = damage

    def damage(self) -> int:
        return self._damage

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._damage == value._damage
                and self._description == value._description
            )
        raise NotImplemented
