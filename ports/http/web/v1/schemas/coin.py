from dataclasses import dataclass

from domain.coin import Coins, PieceType


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
