from typing import Sequence
from uuid import UUID

from domain.coin import Coins
from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName
from domain.weapon.damage import WeaponDamage
from domain.weight import Weight


class Weapon(EntityName, EntityDescription):
    def __init__(
        self,
        weapon_id: UUID,
        weapon_kind: UUID,
        name: str,
        description: str,
        cost: Coins,
        damage: WeaponDamage,
        weight: Weight,
        weapon_properties: Sequence[UUID],
        material_id: UUID,
    ) -> None:
        self.__validate_properties(weapon_properties)
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self.__weapon_id = weapon_id
        self.__kind = weapon_kind
        self.__cost = cost
        self.__damage = damage
        self.__weight = weight
        self.__properties = list(weapon_properties)
        self.__material_id = material_id

    def weapon_id(self) -> UUID:
        return self.__weapon_id

    def kind(self) -> UUID:
        return self.__kind

    def cost(self) -> Coins:
        return self.__cost

    def damage(self) -> WeaponDamage:
        return self.__damage

    def weight(self) -> Weight:
        return self.__weight

    def properties(self) -> list[UUID]:
        return self.__properties

    def material_id(self) -> UUID:
        return self.__material_id

    def new_kind(self, kind: UUID) -> None:
        if self.__kind == kind:
            raise DomainError.idempotent("текущий вид оружия равен новому виду")
        self.__kind = kind

    def new_cost(self, cost: Coins) -> None:
        if self.__cost == cost:
            raise DomainError.idempotent("текущая цена оружия равна новой цене")
        self.__cost = cost

    def new_damage(self, damage: WeaponDamage) -> None:
        if self.__damage == damage:
            raise DomainError.idempotent("текущий урон оружия равен новому урону")
        self.__damage = damage

    def new_weight(self, weight: Weight) -> None:
        if self.__weight == weight:
            raise DomainError.idempotent("текущая масса оружия равна новой массе")
        self.__weight = weight

    def new_properties(self, properties: Sequence[UUID]) -> None:
        if self.__properties == properties:
            raise DomainError.idempotent(
                "текущие свойства оружия равны новым свойствам"
            )
        self.__validate_properties(properties)
        self.__properties = list(properties)

    def new_material_id(self, material_id: UUID) -> None:
        if self.__material_id == material_id:
            raise DomainError.idempotent(
                "текущий материал оружия равен новому материалу"
            )
        self.__material_id = material_id

    def __validate_properties(self, properties: Sequence[UUID]) -> None:
        if len(properties) == 0:
            return
        if len(properties) != len(set(properties)):
            raise DomainError.invalid_data("свойства содержат дубликаты")

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__weapon_id == value.__weapon_id
        if isinstance(value, UUID):
            return self.__weapon_id == value
        raise NotImplemented
