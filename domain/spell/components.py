from typing import Sequence
from uuid import UUID


class SpellComponents:
    def __init__(
        self, verbal: bool, symbolic: bool, material: bool, materials: Sequence[UUID]
    ) -> None:
        self._verbal = verbal
        self._symbolic = symbolic
        self._material = material
        self._materials = list(materials)

    def verbal(self) -> bool:
        return self._verbal

    def symbolic(self) -> bool:
        return self._symbolic

    def material(self) -> bool:
        return self._material

    def materials(self) -> list[UUID]:
        return self._materials

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._verbal == value._verbal
                and self._symbolic == value._symbolic
                and self._material == value._material
                and set(self._materials) == set(value._materials)
            )
        raise NotImplemented
