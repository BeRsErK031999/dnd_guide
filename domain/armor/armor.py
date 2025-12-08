from uuid import UUID

from domain.armor.armor_class import ArmorClass
from domain.armor.armor_type import ArmorType
from domain.coin import Coins
from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName
from domain.weight import Weight


class Armor(EntityName, EntityDescription):
    def __init__(
        self,
        armor_id: UUID,
        armor_type: ArmorType,
        name: str,
        description: str,
        armor_class: ArmorClass,
        strength: int,
        stealth: bool,
        weight: Weight,
        cost: Coins,
        material_id: UUID,
    ) -> None:
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self._validate_strength(strength)
        self._armor_id = armor_id
        self._armor_type = armor_type
        self._armor_class = armor_class
        self._strength = strength
        self._stealth = stealth
        self._weight = weight
        self._cost = cost
        self._material_id = material_id

    def armor_id(self) -> UUID:
        return self._armor_id

    def armor_type(self) -> ArmorType:
        return self._armor_type

    def armor_class(self) -> ArmorClass:
        return self._armor_class

    def strength(self) -> int:
        return self._strength

    def stealth(self) -> bool:
        return self._stealth

    def weight(self) -> Weight:
        return self._weight

    def cost(self) -> Coins:
        return self._cost

    def material_id(self) -> UUID:
        return self._material_id

    def new_armor_type(self, armor_type: ArmorType) -> None:
        if self._armor_type == armor_type:
            raise DomainError.idempotent(
                "текущий тип доспеха равен новому типу доспеха"
            )
        self._armor_type = armor_type

    def new_armor_class(self, armor_class: ArmorClass) -> None:
        if self._armor_class == armor_class:
            raise DomainError.idempotent(
                "текущий класс доспеха равен новому классу доспеха"
            )
        self._armor_class = armor_class

    def new_strength(self, strength: int) -> None:
        if self._strength == strength:
            raise DomainError.idempotent(
                "текущее требование к силе доспеха равно новому требованию к силе доспеха"
            )
        self._validate_strength(strength)
        self._strength = strength

    def new_stealth(self, stealth: bool) -> None:
        if self._stealth == stealth:
            raise DomainError.idempotent(
                "текущая помеха доспеха равно новой помехе доспеха"
            )
        self._stealth = stealth

    def new_weight(self, weight: Weight) -> None:
        if self._weight == weight:
            raise DomainError.idempotent(
                "текущая масса доспеха равна новой массе доспеха"
            )
        self._weight = weight

    def new_cost(self, cost: Coins) -> None:
        if self._cost == cost:
            raise DomainError.idempotent(
                "текущая стоимость доспеха равна новой стоимости доспеха"
            )
        self._cost = cost

    def new_material_id(self, material_id: UUID) -> None:
        if self._material_id == material_id:
            raise DomainError.idempotent(
                "текущий материал доспеха равен новому материалу доспеха"
            )
        self._material_id = material_id

    def _validate_strength(self, strength: int) -> None:
        if strength < 0 or strength > 20:
            raise DomainError.invalid_data(
                "модификатор силы для доспехов должен находиться в диапазоне от 0 до 20"
            )

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._armor_id == value._armor_id
        if isinstance(value, UUID):
            return self._armor_id == value
        raise NotImplemented
