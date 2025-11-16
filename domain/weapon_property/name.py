from enum import StrEnum

from domain.error import DomainError


class WeaponPropertyName(StrEnum):
    AMMUNITION = "боеприпасы"
    FINESSE = "фехтовальное"
    HEAVY = "тяжелое"
    LIGHT = "легкое"
    REACH = "досягаемость"
    SPECIAL = "особое"
    THROWN = "метательное"
    TWO_HANDED = "двуручное"
    VERSATILE = "универсальное"
    DISTANCE = "дистанция"

    @staticmethod
    def from_str(name: str) -> "WeaponPropertyName":
        match name.upper():
            case WeaponPropertyName.AMMUNITION.name:
                return WeaponPropertyName.AMMUNITION
            case WeaponPropertyName.FINESSE.name:
                return WeaponPropertyName.FINESSE
            case WeaponPropertyName.HEAVY.name:
                return WeaponPropertyName.HEAVY
            case WeaponPropertyName.LIGHT.name:
                return WeaponPropertyName.LIGHT
            case WeaponPropertyName.REACH.name:
                return WeaponPropertyName.REACH
            case WeaponPropertyName.SPECIAL.name:
                return WeaponPropertyName.SPECIAL
            case WeaponPropertyName.THROWN.name:
                return WeaponPropertyName.THROWN
            case WeaponPropertyName.TWO_HANDED.name:
                return WeaponPropertyName.TWO_HANDED
            case WeaponPropertyName.VERSATILE.name:
                return WeaponPropertyName.VERSATILE
            case WeaponPropertyName.DISTANCE.name:
                return WeaponPropertyName.DISTANCE
            case _:
                raise DomainError.invalid_data(
                    f"для названия свойства оружия с названием {name} не удалось "
                    "сопоставить значение"
                )
