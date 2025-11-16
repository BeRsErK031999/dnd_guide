from dataclasses import dataclass

from domain.coin import Coins, PieceType


@dataclass
class ReadPieceTypeSchema:
    copper: str
    silver: str
    electrum: str
    gold: str
    platinum: str

    @staticmethod
    def from_domain() -> ReadPieceTypeSchema:
        return ReadPieceTypeSchema(
            **{name.name.lower(): name.value for name in PieceType}
        )


@dataclass
class CoinSchema:
    count: int
    piece_type: str

    @staticmethod
    def from_domain(coin: Coins) -> CoinSchema:
        return CoinSchema(
            count=coin.in_copper(),
            piece_type=PieceType.COPPER.name,
        )
