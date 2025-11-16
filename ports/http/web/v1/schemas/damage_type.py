from dataclasses import dataclass

from domain.damage_type import DamageType


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
    def from_domain() -> "ReadDamageTypeSchema":
        return ReadDamageTypeSchema(
            **{
                damage_type.name.lower(): damage_type.value
                for damage_type in DamageType
            }
        )
