from dataclasses import asdict, dataclass

from application.dto.model.length import AppLength, AppLengthUnit


@dataclass
class ReadLengthUnitSchema:
    ft: str
    m: str

    @staticmethod
    def from_app() -> "ReadLengthUnitSchema":
        return ReadLengthUnitSchema(**asdict(AppLengthUnit.from_domain()))


@dataclass
class LengthSchema:
    count: float
    unit: str

    @staticmethod
    def from_app(length: AppLength) -> "LengthSchema":
        return LengthSchema(count=length.count, unit=length.unit)
