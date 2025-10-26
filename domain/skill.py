from enum import StrEnum

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
