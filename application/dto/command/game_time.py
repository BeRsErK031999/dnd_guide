from dataclasses import dataclass

__all__ = ["GameTimeCommand"]


@dataclass
class GameTimeCommand:
    count: int
    unit: str
