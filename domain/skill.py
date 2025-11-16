from enum import StrEnum

from domain.error import DomainError
from domain.modifier import Modifier


class Skill(StrEnum):
    ACROBATICS = "акробатика"
    ATHLETICS = "атлетика"
    PERCEPTION = "внимание"
    SURVIVAL = "выживание"
    ANIMAL_HANDLING = "дрессировка"
    INTIMIDATION = "запугивание"
    PERFORMANCE = "исполнение"
    HISTORY = "история"
    SLEIGHT_OF_HAND = "ловкость рук"
    ARCANA = "магия"
    MEDICINE = "медицина"
    DECEPTION = "обман"
    NATURE = "природа"
    INSIGHT = "проницательность"
    INVESTIGATION = "расследование"
    RELIGION = "религия"
    STEALTH = "скрытность"
    PERSUASION = "убеждение"

    @staticmethod
    def from_str(name: str) -> "Skill":
        match name.upper():
            case Skill.ACROBATICS.name:
                return Skill.ACROBATICS
            case Skill.ATHLETICS.name:
                return Skill.ATHLETICS
            case Skill.PERCEPTION.name:
                return Skill.PERCEPTION
            case Skill.SURVIVAL.name:
                return Skill.SURVIVAL
            case Skill.ANIMAL_HANDLING.name:
                return Skill.ANIMAL_HANDLING
            case Skill.INTIMIDATION.name:
                return Skill.INTIMIDATION
            case Skill.PERFORMANCE.name:
                return Skill.PERFORMANCE
            case Skill.HISTORY.name:
                return Skill.HISTORY
            case Skill.SLEIGHT_OF_HAND.name:
                return Skill.SLEIGHT_OF_HAND
            case Skill.ARCANA.name:
                return Skill.ARCANA
            case Skill.MEDICINE.name:
                return Skill.MEDICINE
            case Skill.DECEPTION.name:
                return Skill.DECEPTION
            case Skill.NATURE.name:
                return Skill.NATURE
            case Skill.INSIGHT.name:
                return Skill.INSIGHT
            case Skill.INVESTIGATION.name:
                return Skill.INVESTIGATION
            case Skill.RELIGION.name:
                return Skill.RELIGION
            case Skill.STEALTH.name:
                return Skill.STEALTH
            case Skill.PERSUASION.name:
                return Skill.PERSUASION
            case _:
                raise DomainError.invalid_data(
                    f"для навыка с названием {name} не удалось сопоставить значение"
                )

    def modifier(self) -> Modifier:
        match self:
            case Skill.ATHLETICS:
                return Modifier.STRENGTH

            case Skill.ACROBATICS | Skill.SLEIGHT_OF_HAND | Skill.STEALTH:
                return Modifier.DEXTERITY

            case (
                Skill.ARCANA
                | Skill.HISTORY
                | Skill.INVESTIGATION
                | Skill.NATURE
                | Skill.RELIGION
            ):
                return Modifier.INTELLECT

            case (
                Skill.ANIMAL_HANDLING
                | Skill.INSIGHT
                | Skill.MEDICINE
                | Skill.PERCEPTION
                | Skill.SURVIVAL
            ):
                return Modifier.WISDOM

            case (
                Skill.DECEPTION
                | Skill.INTIMIDATION
                | Skill.PERFORMANCE
                | Skill.PERSUASION
            ):
                return Modifier.CHARISMA
