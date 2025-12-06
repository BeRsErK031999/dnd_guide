from dataclasses import dataclass

from domain.skill import Skill


@dataclass
class AppSkill:
    value: str
    modifier: str

    @staticmethod
    def from_domain(skill: Skill) -> "AppSkill":
        return AppSkill(value=skill.value, modifier=skill.modifier().value)


@dataclass
class AppSkills:
    acrobatics: AppSkill
    athletics: AppSkill
    perception: AppSkill
    survival: AppSkill
    animal_handling: AppSkill
    intimidation: AppSkill
    performance: AppSkill
    history: AppSkill
    sleight_of_hand: AppSkill
    arcana: AppSkill
    medicine: AppSkill
    deception: AppSkill
    nature: AppSkill
    insight: AppSkill
    investigation: AppSkill
    religion: AppSkill
    stealth: AppSkill
    persuasion: AppSkill

    @staticmethod
    def from_domain() -> "AppSkills":
        return AppSkills(
            **{skill.name.lower(): AppSkill.from_domain(skill) for skill in Skill}
        )
