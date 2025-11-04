from dataclasses import dataclass


@dataclass
class WeightCommand:
    count: float
    unit: str
