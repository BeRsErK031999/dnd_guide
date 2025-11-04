from dataclasses import dataclass


@dataclass
class CoinCommand:
    count: int
    piece_type: str
