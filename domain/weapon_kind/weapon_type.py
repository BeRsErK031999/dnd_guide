from enum import StrEnum

from domain.error import DomainError


class WeaponType(StrEnum):
    SIMPLE_RANGE = "простое дистанционное"
    SIMPLE_MELEE = "простое рукопашное"
    MARTIAL_RANGE = "воинское дистанционное"
    MARTIAL_MELEE = "воинское рукопашное"

    @staticmethod
    def from_str(name: str) -> WeaponType:
        match name.upper():
            case WeaponType.SIMPLE_RANGE.name:
                return WeaponType.SIMPLE_RANGE
            case WeaponType.SIMPLE_MELEE.name:
                return WeaponType.SIMPLE_MELEE
            case WeaponType.MARTIAL_RANGE.name:
                return WeaponType.MARTIAL_RANGE
            case WeaponType.MARTIAL_MELEE.name:
                return WeaponType.MARTIAL_MELEE
            case _:
                raise DomainError.invalid_data(
                    f"для типа оружия с названием {name} не удалось "
                    "сопоставить значение"
                )
