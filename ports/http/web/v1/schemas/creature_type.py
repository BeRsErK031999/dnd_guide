from dataclasses import asdict, dataclass

from application.dto.model.creature_type import AppCreatureType


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
    def from_app() -> "ReadCreatureTypeSchema":
        return ReadCreatureTypeSchema(**asdict(AppCreatureType.from_domain()))
