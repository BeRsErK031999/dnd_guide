from enum import StrEnum

from domain.error import DomainError


class CreatureType(StrEnum):
    ABERRATION = "аберрация"
    BEAST = "зверь"
    CELESTIAL = "небожитель"
    CONSTRUCT = "конструкт"
    DRAGON = "дракон"
    ELEMENTAL = "элементаль"
    FEY = "фея"
    FIEND = "исчадие"
    GIANT = "великан"
    HUMANOID = "гуманоид"
    MONSTROSITY = "чудовище"
    OOZE = "слизь"
    PLANT = "растение"
    UNDEAD = "нежить"
    TRANSPORT = "транспорт"
    OBJECT = "объект"

    @staticmethod
    def from_str(name: str) -> "CreatureType":
        match name.upper():
            case CreatureType.ABERRATION.name:
                return CreatureType.ABERRATION
            case CreatureType.BEAST.name:
                return CreatureType.BEAST
            case CreatureType.CELESTIAL.name:
                return CreatureType.CELESTIAL
            case CreatureType.CONSTRUCT.name:
                return CreatureType.CONSTRUCT
            case CreatureType.DRAGON.name:
                return CreatureType.DRAGON
            case CreatureType.ELEMENTAL.name:
                return CreatureType.ELEMENTAL
            case CreatureType.FEY.name:
                return CreatureType.FEY
            case CreatureType.FIEND.name:
                return CreatureType.FIEND
            case CreatureType.GIANT.name:
                return CreatureType.GIANT
            case CreatureType.HUMANOID.name:
                return CreatureType.HUMANOID
            case CreatureType.MONSTROSITY.name:
                return CreatureType.MONSTROSITY
            case CreatureType.OOZE.name:
                return CreatureType.OOZE
            case CreatureType.PLANT.name:
                return CreatureType.PLANT
            case CreatureType.UNDEAD.name:
                return CreatureType.UNDEAD
            case CreatureType.TRANSPORT.name:
                return CreatureType.TRANSPORT
            case CreatureType.OBJECT.name:
                return CreatureType.OBJECT
            case _:
                raise DomainError.invalid_data(
                    f"для типа существа с названием {name} не удалось "
                    "сопоставить значение"
                )
