from dataclasses import dataclass

from domain.game_time import GameTime, GameTimeUnit


@dataclass
class ReadGameTimeUnitSchema:
    action: str
    bonus_action: str
    reaction: str
    minute: str
    hour: str

    @staticmethod
    def from_domain() -> "ReadGameTimeUnitSchema":
        return ReadGameTimeUnitSchema(
            **{name.name.lower(): name.value for name in GameTimeUnit}
        )


@dataclass
class GameTimeSchema:
    count: int
    unit: str

    @staticmethod
    def from_domain(game_time: GameTime) -> "GameTimeSchema":
        return GameTimeSchema(count=game_time.count(), unit=game_time.units().name)
