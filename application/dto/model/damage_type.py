from dataclasses import dataclass

from domain.damage_type import DamageType


@dataclass
class AppDamageType:
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
    def from_domain() -> "AppDamageType":
        return AppDamageType(
            **{
                damage_type.name.lower(): damage_type.value
                for damage_type in DamageType
            }
        )
