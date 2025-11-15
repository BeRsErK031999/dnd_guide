from dataclasses import dataclass

from domain.game_time import GameTime


@dataclass
class GameTimeSchema:
    count: int
    unit: str

    @staticmethod
    def from_domain(game_time: GameTime) -> GameTimeSchema:
        return GameTimeSchema(count=game_time.count(), unit=game_time.units().name)
