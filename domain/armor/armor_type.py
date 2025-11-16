from enum import StrEnum

from domain.error import DomainError


class ArmorType(StrEnum):
    LIGHT_ARMOR = "лёгкий доспех"
    MEDIUM_ARMOR = "средний доспех"
    HEAVY_ARMOR = "тяжёлый доспех"
    SHIELD = "щит"

    @staticmethod
    def from_str(name: str) -> ArmorType:
        match name.upper():
            case ArmorType.LIGHT_ARMOR.name:
                return ArmorType.LIGHT_ARMOR
            case ArmorType.MEDIUM_ARMOR.name:
                return ArmorType.MEDIUM_ARMOR
            case ArmorType.HEAVY_ARMOR.name:
                return ArmorType.HEAVY_ARMOR
            case ArmorType.SHIELD.name:
                return ArmorType.SHIELD
            case _:
                raise DomainError.invalid_data(
                    f"для типа доспехов с названием {name} не удалось сопоставить значение"
                )
