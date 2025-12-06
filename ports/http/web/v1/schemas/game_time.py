from dataclasses import asdict, dataclass

from application.dto.command.game_time import GameTimeCommand
from application.dto.model.game_time import AppGameTime, AppGameTimeUnit


@dataclass
class ReadGameTimeUnitSchema:
    action: str
    bonus_action: str
    reaction: str
    minute: str
    hour: str

    @staticmethod
    def from_app() -> "ReadGameTimeUnitSchema":
        return ReadGameTimeUnitSchema(**asdict(AppGameTimeUnit.from_domain()))


@dataclass
class GameTimeSchema:
    count: int
    unit: str

    @staticmethod
    def from_app(game_time: AppGameTime) -> "GameTimeSchema":
        return GameTimeSchema(count=game_time.count, unit=game_time.unit)

    def to_command(self) -> GameTimeCommand:
        return GameTimeCommand(count=self.count, unit=self.unit)
