from dataclasses import asdict, dataclass

from application.dto.command.dice import DiceCommand
from application.dto.model.dice import AppDice, AppDiceType


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
    def from_app() -> "ReadDiceTypeSchema":
        return ReadDiceTypeSchema(**asdict(AppDiceType.from_domain()))


@dataclass
class DiceSchema:
    count: int
    dice_type: str

    @staticmethod
    def from_app(dice: AppDice) -> "DiceSchema":
        return DiceSchema(count=dice.count, dice_type=dice.dice_type)

    def to_command(self) -> DiceCommand:
        return DiceCommand(count=self.count, dice_type=self.dice_type)
