from enum import StrEnum

from domain.modifier import Modifier


class ClassSkill(StrEnum):
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

    def modifier(self) -> Modifier:
        match self:
            case ClassSkill.ATHLETICS:
                return Modifier.STRENGTH

            case (
                ClassSkill.ACROBATICS | ClassSkill.SLEIGHT_OF_HAND | ClassSkill.STEALTH
            ):
                return Modifier.DEXTERITY

            case (
                ClassSkill.ARCANA
                | ClassSkill.HISTORY
                | ClassSkill.INVESTIGATION
                | ClassSkill.NATURE
                | ClassSkill.RELIGION
            ):
                return Modifier.INTELLIGENT

            case (
                ClassSkill.ANIMAL_HANDLING
                | ClassSkill.INSIGHT
                | ClassSkill.MEDICINE
                | ClassSkill.PERCEPTION
                | ClassSkill.SURVIVAL
            ):
                return Modifier.WISDOM

            case (
                ClassSkill.DECEPTION
                | ClassSkill.INTIMIDATION
                | ClassSkill.PERFORMANCE
                | ClassSkill.PERSUASION
            ):
                return Modifier.CHARISMA
