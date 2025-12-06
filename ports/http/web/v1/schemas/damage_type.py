from dataclasses import asdict, dataclass

from application.dto.model.damage_type import AppDamageType


@dataclass
class ReadDamageTypeSchema:
    acid: str
    bludgeoning: str
    cold: str
    fire: str
    force: str
    lightning: str
    necrotic: str
    piercing: str
    poison: str
    psychic: str
    radiant: str
    slashing: str
    thunder: str

    @staticmethod
    def from_app() -> "ReadDamageTypeSchema":
        return ReadDamageTypeSchema(**asdict(AppDamageType.from_domain()))
