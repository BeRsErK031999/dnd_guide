from dataclasses import dataclass

from domain.weight import Weight, WeightUnit


@dataclass
class WeightSchema:
    count: float
    unit: str

    @staticmethod
    def from_domain(weight: Weight) -> WeightSchema:
        return WeightSchema(
            count=weight.in_lb(),
            unit=WeightUnit.LB.value,
        )
