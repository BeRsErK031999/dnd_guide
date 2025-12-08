from dataclasses import dataclass

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
        app_skills = AppSkills.from_domain()
        return ReadSkillSchema(
            acrobatics=SkillSchema.from_app(app_skills.acrobatics),
            athletics=SkillSchema.from_app(app_skills.athletics),
            perception=SkillSchema.from_app(app_skills.perception),
            survival=SkillSchema.from_app(app_skills.survival),
            animal_handling=SkillSchema.from_app(app_skills.animal_handling),
            intimidation=SkillSchema.from_app(app_skills.intimidation),
            performance=SkillSchema.from_app(app_skills.performance),
            history=SkillSchema.from_app(app_skills.history),
            sleight_of_hand=SkillSchema.from_app(app_skills.sleight_of_hand),
            arcana=SkillSchema.from_app(app_skills.arcana),
            medicine=SkillSchema.from_app(app_skills.medicine),
            deception=SkillSchema.from_app(app_skills.deception),
            nature=SkillSchema.from_app(app_skills.nature),
            insight=SkillSchema.from_app(app_skills.insight),
            investigation=SkillSchema.from_app(app_skills.investigation),
            religion=SkillSchema.from_app(app_skills.religion),
            stealth=SkillSchema.from_app(app_skills.stealth),
            persuasion=SkillSchema.from_app(app_skills.persuasion),
        )
