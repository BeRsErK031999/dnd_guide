from dataclasses import dataclass

from domain.creature_size import CreatureSize


@dataclass
class ReadCreatureSizeSchema:
    tiny: str
    small: str
    medium: str
    large: str
    huge: str
    gargantuan: str

    @staticmethod
    def from_domain() -> "ReadCreatureSizeSchema":
        return ReadCreatureSizeSchema(
            **{size.name.lower(): size.value for size in CreatureSize}
        )
