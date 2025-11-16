from dataclasses import dataclass

from domain.modifier import Modifier


@dataclass
class ReadModifierSchema:
    strength: str
    dexterity: str
    constitution: str
    intellect: str
    wisdom: str
    charisma: str

    @staticmethod
    def from_domain() -> ReadModifierSchema:
        return ReadModifierSchema(
            **{modifier.name.lower(): modifier.value for modifier in Modifier}
        )
