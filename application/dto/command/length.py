from dataclasses import dataclass

__all__ = ["LengthCommand"]


@dataclass
class LengthCommand:
    count: float
    unit: str
