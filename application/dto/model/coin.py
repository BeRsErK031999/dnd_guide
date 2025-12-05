from dataclasses import dataclass

from domain.coin import Coins, PieceType


@dataclass
class AppPieceType:
    copper: str
    silver: str
    electrum: str
    gold: str
    platinum: str

    @staticmethod
    def from_domain() -> "AppPieceType":
        return AppPieceType(**{name.name.lower(): name.value for name in PieceType})


@dataclass
class AppCoins:
    count: int
    piece_type: str

    @staticmethod
    def from_domain(coin: Coins) -> "AppCoins":
        return AppCoins(
            count=coin.in_copper(),
            piece_type=PieceType.COPPER.name,
        )

    def to_domain(self) -> Coins:
        return Coins(count=self.count, piece_type=PieceType.from_str(self.piece_type))
