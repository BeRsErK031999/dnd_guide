from dataclasses import dataclass

from domain.length import Length, LengthUnit


@dataclass
class LengthSchema:
    count: float
    unit: str

    @staticmethod
    def from_domain(length: Length) -> LengthSchema:
        return LengthSchema(count=length.in_ft(), unit=LengthUnit.FT.value)
