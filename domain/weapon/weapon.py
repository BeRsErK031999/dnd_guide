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
        weapon_kind_id: UUID,
        name: str,
        description: str,
        cost: Coins,
        damage: WeaponDamage,
        weight: Weight,
        weapon_property_ids: Sequence[UUID],
        material_id: UUID,
    ) -> None:
        self._validate_property_ids(weapon_property_ids)
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self._weapon_id = weapon_id
        self._kind_id = weapon_kind_id
        self._cost = cost
        self._damage = damage
        self._weight = weight
        self._property_ids = list(weapon_property_ids)
        self._material_id = material_id

    def weapon_id(self) -> UUID:
        return self._weapon_id

    def kind_id(self) -> UUID:
        return self._kind_id

    def cost(self) -> Coins:
        return self._cost

    def damage(self) -> WeaponDamage:
        return self._damage

    def weight(self) -> Weight:
        return self._weight

    def property_ids(self) -> list[UUID]:
        return self._property_ids

    def material_id(self) -> UUID:
        return self._material_id

    def new_kind_id(self, kind: UUID) -> None:
        if self._kind_id == kind:
            raise DomainError.idempotent("текущий вид оружия равен новому виду")
        self._kind_id = kind

    def new_cost(self, cost: Coins) -> None:
        if self._cost == cost:
            raise DomainError.idempotent("текущая цена оружия равна новой цене")
        self._cost = cost

    def new_damage(self, damage: WeaponDamage) -> None:
        if self._damage == damage:
            raise DomainError.idempotent("текущий урон оружия равен новому урону")
        self._damage = damage

    def new_weight(self, weight: Weight) -> None:
        if self._weight == weight:
            raise DomainError.idempotent("текущая масса оружия равна новой массе")
        self._weight = weight

    def new_property_ids(self, property_ids: Sequence[UUID]) -> None:
        if self._property_ids == property_ids:
            raise DomainError.idempotent(
                "текущие свойства оружия равны новым свойствам"
            )
        self._validate_property_ids(property_ids)
        self._property_ids = list(property_ids)

    def new_material_id(self, material_id: UUID) -> None:
        if self._material_id == material_id:
            raise DomainError.idempotent(
                "текущий материал оружия равен новому материалу"
            )
        self._material_id = material_id

    def _validate_property_ids(self, properties: Sequence[UUID]) -> None:
        if len(properties) == 0:
            return
        if len(properties) != len(set(properties)):
            raise DomainError.invalid_data("свойства содержат дубликаты")

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._weapon_id == value._weapon_id
        if isinstance(value, UUID):
            return self._weapon_id == value
        raise NotImplemented
