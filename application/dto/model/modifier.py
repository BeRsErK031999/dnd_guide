from dataclasses import dataclass

from domain.modifier import Modifier


@dataclass
class AppModifier:
    strength: str
    dexterity: str
    constitution: str
    intellect: str
    wisdom: str
    charisma: str

    @staticmethod
    def from_domain() -> "AppModifier":
        return AppModifier(
            **{modifier.name.lower(): modifier.value for modifier in Modifier}
        )
