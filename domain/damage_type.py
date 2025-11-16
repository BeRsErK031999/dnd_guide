from enum import StrEnum

from domain.error import DomainError


class DamageType(StrEnum):
    ACID = "кислота"
    BLUDGEONING = "дробящий"
    COLD = "холод"
    FIRE = "огонь"
    FORCE = "силовое поле"
    LIGHTNING = "электричество"
    NECROTIC = "некротическая"
    PIERCING = "колющий"
    POISON = "яд"
    PSYCHIC = "психический"
    RADIANT = "излучение"
    SLASHING = "рубящий"
    THUNDER = "звук"

    @staticmethod
    def from_str(name: str) -> "DamageType":
        match name.upper():
            case DamageType.ACID.name:
                return DamageType.ACID
            case DamageType.BLUDGEONING.name:
                return DamageType.BLUDGEONING
            case DamageType.COLD.name:
                return DamageType.COLD
            case DamageType.FIRE.name:
                return DamageType.FIRE
            case DamageType.FORCE.name:
                return DamageType.FORCE
            case DamageType.LIGHTNING.name:
                return DamageType.LIGHTNING
            case DamageType.NECROTIC.name:
                return DamageType.NECROTIC
            case DamageType.PIERCING.name:
                return DamageType.PIERCING
            case DamageType.POISON.name:
                return DamageType.POISON
            case DamageType.PSYCHIC.name:
                return DamageType.PSYCHIC
            case DamageType.RADIANT.name:
                return DamageType.RADIANT
            case DamageType.SLASHING.name:
                return DamageType.SLASHING
            case DamageType.THUNDER.name:
                return DamageType.THUNDER
            case _:
                raise DomainError.invalid_data(
                    f"для типа урона с названием {name} не удалось "
                    "сопоставить значение"
                )
