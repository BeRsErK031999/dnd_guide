from dataclasses import dataclass


@dataclass
class LengthCommand:
    count: float
    unit: str
