from domain.mixin import ValueDescription


class ClassLevelBonusDamage(ValueDescription):
    def __init__(self, bonus_damage: int, bonus_damage_description: str) -> None:
        ValueDescription.__init__(self, bonus_damage_description)
        self.__damage = bonus_damage

    def damage(self) -> int:
        return self.__damage

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__damage == value.__damage
                and self.__description == value.__description
            )
        raise NotImplemented
