from dataclasses import asdict, dataclass

from application.dto.model.modifier import AppModifier


@dataclass
class ReadModifierSchema:
    strength: str
    dexterity: str
    constitution: str
    intellect: str
    wisdom: str
    charisma: str

    @staticmethod
    def from_app() -> "ReadModifierSchema":
        return ReadModifierSchema(**asdict(AppModifier.from_domain()))
