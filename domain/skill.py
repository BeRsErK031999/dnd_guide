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
    def from_str(name: str) -> Skill:
        match name:
            case Skill.ACROBATICS.value:
                return Skill.ACROBATICS
            case Skill.ATHLETICS.value:
                return Skill.ATHLETICS
            case Skill.PERCEPTION.value:
                return Skill.PERCEPTION
            case Skill.SURVIVAL.value:
                return Skill.SURVIVAL
            case Skill.ANIMAL_HANDLING.value:
                return Skill.ANIMAL_HANDLING
            case Skill.INTIMIDATION.value:
                return Skill.INTIMIDATION
            case Skill.PERFORMANCE.value:
                return Skill.PERFORMANCE
            case Skill.HISTORY.value:
                return Skill.HISTORY
            case Skill.SLEIGHT_OF_HAND.value:
                return Skill.SLEIGHT_OF_HAND
            case Skill.ARCANA.value:
                return Skill.ARCANA
            case Skill.MEDICINE.value:
                return Skill.MEDICINE
            case Skill.DECEPTION.value:
                return Skill.DECEPTION
            case Skill.NATURE.value:
                return Skill.NATURE
            case Skill.INSIGHT.value:
                return Skill.INSIGHT
            case Skill.INVESTIGATION.value:
                return Skill.INVESTIGATION
            case Skill.RELIGION.value:
                return Skill.RELIGION
            case Skill.STEALTH.value:
                return Skill.STEALTH
            case Skill.PERSUASION.value:
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
                return Modifier.INTELLIGENT

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
