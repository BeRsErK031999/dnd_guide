from dataclasses import asdict, dataclass

from application.dto.command.coin import CoinCommand
from application.dto.model.coin import AppCoins, AppPieceType


@dataclass
class ReadPieceTypeSchema:
    copper: str
    silver: str
    electrum: str
    gold: str
    platinum: str

    @staticmethod
    def from_app() -> "ReadPieceTypeSchema":
        return ReadPieceTypeSchema(**asdict(AppPieceType.from_domain()))


@dataclass
class CoinSchema:
    count: int
    piece_type: str

    @staticmethod
    def from_app(coin: AppCoins) -> "CoinSchema":
        return CoinSchema(count=coin.count, piece_type=coin.piece_type)

    def to_command(self) -> CoinCommand:
        return CoinCommand(count=self.count, piece_type=self.piece_type)
