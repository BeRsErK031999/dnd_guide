from dataclasses import dataclass

from domain.dice import Dice


@dataclass
class DiceSchema:
    count: int
    dice_type: str

    @staticmethod
    def from_domain(dice: Dice) -> DiceSchema:
        return DiceSchema(
            count=dice.count(),
            dice_type=dice.dice_type().name,
        )
