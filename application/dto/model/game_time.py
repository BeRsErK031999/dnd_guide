from dataclasses import dataclass

from domain.game_time import GameTime, GameTimeUnit

__all__ = ["AppGameTime", "AppGameTimeUnit"]


@dataclass
class AppGameTimeUnit:
    action: str
    bonus_action: str
    reaction: str
    minute: str
    hour: str

    @staticmethod
    def from_domain() -> "AppGameTimeUnit":
        return AppGameTimeUnit(
            **{name.name.lower(): name.value for name in GameTimeUnit}
        )


@dataclass
class AppGameTime:
    count: int
    unit: str

    @staticmethod
    def from_domain(game_time: GameTime) -> "AppGameTime":
        return AppGameTime(count=game_time.count(), unit=game_time.units().name.lower())

    def to_domain(self) -> GameTime:
        return GameTime(count=self.count, units=GameTimeUnit.from_str(self.unit))
