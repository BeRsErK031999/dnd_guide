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
        strength: int | None,
        stealth: bool,
        weight: Weight,
        cost: Coins,
    ) -> None:
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self.__validate_strength(strength)
        self.__armor_id = armor_id
        self.__armor_type = armor_type
        self.__armor_class = armor_class
        self.__strength = strength
        self.__stealth = stealth
        self.__weight = weight
        self.__cost = cost

    def armor_id(self) -> UUID:
        return self.__armor_id

    def armor_type(self) -> ArmorType:
        return self.__armor_type

    def armor_class(self) -> ArmorClass:
        return self.__armor_class

    def strength(self) -> int | None:
        return self.__strength

    def stealth(self) -> bool:
        return self.__stealth

    def weight(self) -> Weight:
        return self.__weight

    def cost(self) -> Coins:
        return self.__cost

    def new_armor_type(self, armor_type: ArmorType) -> None:
        if self.__armor_type == armor_type:
            raise DomainError.idempotent(
                "текущий тип доспеха равен новому типу доспеха"
            )
        self.__armor_type = armor_type

    def new_armor_class(self, armor_class: ArmorClass) -> None:
        if self.__armor_class == armor_class:
            raise DomainError.idempotent(
                "текущий класс доспеха равен новому классу доспеха"
            )
        self.__armor_class = armor_class

    def new_strength(self, strength: int | None) -> None:
        if self.__strength == strength:
            raise DomainError.idempotent(
                "текущее требование к силе доспеха равно новому требованию к силе доспеха"
            )
        self.__validate_strength(strength)
        self.__strength = strength

    def new_stealth(self, stealth: bool) -> None:
        if self.__stealth == stealth:
            raise DomainError.idempotent(
                "текущая помеха доспеха равно новой помехе доспеха"
            )
        self.__stealth = stealth

    def new_weight(self, weight: Weight) -> None:
        if self.__weight == weight:
            raise DomainError.idempotent(
                "текущая масса доспеха равна новой массе доспеха"
            )
        self.__weight = weight

    def new_cost(self, cost: Coins) -> None:
        if self.__cost == cost:
            raise DomainError.idempotent(
                "текущая стоимость доспеха равна новой стоимости доспеха"
            )
        self.__cost = cost

    def __validate_strength(self, strength: int | None) -> None:
        if strength is None:
            return
        if strength < 1 or strength > 20:
            raise DomainError.invalid_data(
                "модификатор силы для доспехов должен находиться в диапазоне от 1 до 20"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__armor_id == value.__armor_id
        if isinstance(value, UUID):
            return self.__armor_id == value
        raise NotImplemented
