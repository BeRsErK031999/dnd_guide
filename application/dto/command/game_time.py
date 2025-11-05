from dataclasses import dataclass


@dataclass
class GameTimeCommand:
    count: int
    unit: str
