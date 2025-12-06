from dataclasses import asdict, dataclass

from application.dto.model.creature_size import AppCreatureSize


@dataclass
class ReadCreatureSizeSchema:
    tiny: str
    small: str
    medium: str
    large: str
    huge: str
    gargantuan: str

    @staticmethod
    def from_app() -> "ReadCreatureSizeSchema":
        return ReadCreatureSizeSchema(**asdict(AppCreatureSize.from_domain()))
