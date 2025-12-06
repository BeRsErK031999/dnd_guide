from dataclasses import asdict, dataclass

from application.dto.model.weight import AppWeight, AppWeightUnit


@dataclass
class ReadWeightUnitSchema:
    lb: str
    kg: str

    @staticmethod
    def from_app() -> "ReadWeightUnitSchema":
        return ReadWeightUnitSchema(**asdict(AppWeightUnit.from_domain()))


@dataclass
class WeightSchema:
    count: float
    unit: str

    @staticmethod
    def from_app(weight: AppWeight) -> "WeightSchema":
        return WeightSchema(count=weight.count, unit=weight.unit)
