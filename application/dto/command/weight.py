from dataclasses import dataclass

__all__ = ["WeightCommand"]


@dataclass
class WeightCommand:
    count: float
    unit: str
