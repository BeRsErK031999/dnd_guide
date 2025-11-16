from dataclasses import dataclass

from domain.weight import Weight, WeightUnit


@dataclass
class ReadWeightUnitSchema:
    lb: str
    kg: str

    @staticmethod
    def from_domain() -> "ReadWeightUnitSchema":
        return ReadWeightUnitSchema(lb=WeightUnit.LB.value, kg=WeightUnit.KG.value)


@dataclass
class WeightSchema:
    count: float
    unit: str

    @staticmethod
    def from_domain(weight: Weight) -> "WeightSchema":
        return WeightSchema(
            count=weight.in_lb(),
            unit=WeightUnit.LB.value,
        )
