from dataclasses import dataclass

from domain.dice import Dice, DiceType

__all__ = ["AppDice", "AppDiceType"]


@dataclass
class AppDiceType:
    d4: int
    d6: int
    d8: int
    d10: int
    d12: int
    d20: int
    d100: int

    @staticmethod
    def from_domain() -> "AppDiceType":
        return AppDiceType(
            **{dice_type.name.lower(): dice_type.value for dice_type in DiceType}
        )


@dataclass
class AppDice:
    count: int
    dice_type: str

    @staticmethod
    def from_domain(dice: Dice) -> "AppDice":
        return AppDice(
            count=dice.count(),
            dice_type=dice.dice_type().name.lower(),
        )

    def to_domain(self) -> Dice:
        return Dice(count=self.count, dice_type=DiceType.from_str(self.dice_type))
