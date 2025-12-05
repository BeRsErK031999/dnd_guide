from dataclasses import dataclass

from domain.length import Length, LengthUnit


@dataclass
class AppLengthUnit:
    ft: str
    m: str

    @staticmethod
    def from_domain() -> "AppLengthUnit":
        return AppLengthUnit(ft=LengthUnit.FT.value, m=LengthUnit.M.value)


@dataclass
class AppLength:
    count: float
    unit: str = LengthUnit.FT.name.lower()

    @staticmethod
    def from_domain(length: Length) -> "AppLength":
        return AppLength(count=length.in_ft(), unit=LengthUnit.FT.name.lower())

    def to_domain(self) -> Length:
        return Length(count=self.count, unit=LengthUnit.from_str(self.unit))
