from typing import Sequence
from uuid import UUID


class SpellComponents:
    def __init__(
        self, verbal: bool, symbolic: bool, material: bool, materials: Sequence[UUID]
    ) -> None:
        self.__verbal = verbal
        self.__symbolic = symbolic
        self.__material = material
        self.__materials = list(materials)

    def verbal(self) -> bool:
        return self.__verbal

    def symbolic(self) -> bool:
        return self.__symbolic

    def material(self) -> bool:
        return self.__material

    def materials(self) -> list[UUID]:
        return self.__materials

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__verbal == value.__verbal
                and self.__symbolic == value.__symbolic
                and self.__material == value.__material
                and set(self.__materials) == set(value.__materials)
            )
        raise NotImplemented
