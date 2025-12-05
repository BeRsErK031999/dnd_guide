from dataclasses import dataclass

from domain.weight import Weight, WeightUnit


@dataclass
class AppWeightUnit:
    lb: str
    kg: str

    @staticmethod
    def from_domain() -> "AppWeightUnit":
        return AppWeightUnit(lb=WeightUnit.LB.value, kg=WeightUnit.KG.value)


@dataclass
class AppWeight:
    count: float
    unit: str = WeightUnit.LB.name.lower()

    @staticmethod
    def from_domain(weight: Weight) -> "AppWeight":
        return AppWeight(
            count=weight.in_lb(),
            unit=WeightUnit.LB.name.lower(),
        )

    def to_domain(self) -> Weight:
        return Weight(count=self.count, unit=WeightUnit.from_str(self.unit))
