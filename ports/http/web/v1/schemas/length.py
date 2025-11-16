from dataclasses import dataclass

from domain.length import Length, LengthUnit


@dataclass
class ReadLengthUnitSchema:
    ft: str
    m: str

    @staticmethod
    def from_domain() -> ReadLengthUnitSchema:
        return ReadLengthUnitSchema(ft=LengthUnit.FT.value, m=LengthUnit.M.value)


@dataclass
class LengthSchema:
    count: float
    unit: str

    @staticmethod
    def from_domain(length: Length) -> LengthSchema:
        return LengthSchema(count=length.in_ft(), unit=LengthUnit.FT.value)
