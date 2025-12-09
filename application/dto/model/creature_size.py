from dataclasses import dataclass

from domain.creature_size import CreatureSize

__all__ = ["AppCreatureSize"]


@dataclass
class AppCreatureSize:
    tiny: str
    small: str
    medium: str
    large: str
    huge: str
    gargantuan: str

    @staticmethod
    def from_domain() -> "AppCreatureSize":
        return AppCreatureSize(
            **{size.name.lower(): size.value for size in CreatureSize}
        )
