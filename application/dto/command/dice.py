from dataclasses import dataclass


@dataclass
class DiceCommand:
    count: int
    dice_type: str
