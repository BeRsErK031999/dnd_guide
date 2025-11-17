from dataclasses import dataclass

from domain.creature_type import CreatureType


@dataclass
class ReadCreatureTypeSchema:
    aberration: str
    beast: str
    celestial: str
    construct: str
    dragon: str
    elemental: str
    fey: str
    fiend: str
    giant: str
    humanoid: str
    monstrosity: str
    ooze: str
    plant: str
    undead: str
    transport: str
    object: str

    @staticmethod
    def from_domain() -> "ReadCreatureTypeSchema":
        return ReadCreatureTypeSchema(
            **{
                creature_type.name.lower(): creature_type.value
                for creature_type in CreatureType
            }
        )
