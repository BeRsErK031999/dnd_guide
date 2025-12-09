from dataclasses import dataclass

__all__ = ["DiceCommand"]


@dataclass
class DiceCommand:
    count: int
    dice_type: str
