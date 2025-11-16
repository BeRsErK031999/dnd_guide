from dataclasses import dataclass

from domain.skill import Skill


@dataclass
class SkillSchema:
    value: str
    modifiers: str

    @staticmethod
    def from_domain(skill: Skill) -> SkillSchema:
        return SkillSchema(value=skill.value, modifiers=skill.modifier().value)


@dataclass
class ReadSkillSchema:
    acrobatics: SkillSchema
    athletics: SkillSchema
    perception: SkillSchema
    survival: SkillSchema
    animal_handling: SkillSchema
    intimidation: SkillSchema
    performance: SkillSchema
    history: SkillSchema
    sleight_of_hand: SkillSchema
    arcana: SkillSchema
    medicine: SkillSchema
    deception: SkillSchema
    nature: SkillSchema
    insight: SkillSchema
    investigation: SkillSchema
    religion: SkillSchema
    stealth: SkillSchema
    persuasion: SkillSchema

    @staticmethod
    def from_domain() -> ReadSkillSchema:
        return ReadSkillSchema(
            **{skill.name.lower(): SkillSchema.from_domain(skill) for skill in Skill}
        )
