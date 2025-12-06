from dataclasses import asdict, dataclass

from application.dto.model.skill import AppSkill, AppSkills


@dataclass
class SkillSchema:
    value: str
    modifier: str

    @staticmethod
    def from_app(skill: AppSkill) -> "SkillSchema":
        return SkillSchema(value=skill.value, modifier=skill.modifier)


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
    def from_app() -> "ReadSkillSchema":
        return ReadSkillSchema(
            **{
                skill: SkillSchema.from_app(st)
                for skill, st in asdict(AppSkills.from_domain()).items()
            }
        )
