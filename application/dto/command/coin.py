from dataclasses import dataclass

__all__ = ["CoinCommand"]


@dataclass
class CoinCommand:
    count: int
    piece_type: str
