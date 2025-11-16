from dataclasses import dataclass

from domain.dice import Dice, DiceType


@dataclass
class ReadDiceTypeSchema:
    d4: int
    d6: int
    d8: int
    d10: int
    d12: int
    d20: int
    d100: int

    @staticmethod
    def from_domain() -> "ReadDiceTypeSchema":
        return ReadDiceTypeSchema(
            **{dice_type.name.lower(): dice_type.value for dice_type in DiceType}
        )


@dataclass
class DiceSchema:
    count: int
    dice_type: str

    @staticmethod
    def from_domain(dice: Dice) -> "DiceSchema":
        return DiceSchema(
            count=dice.count(),
            dice_type=dice.dice_type().name,
        )
