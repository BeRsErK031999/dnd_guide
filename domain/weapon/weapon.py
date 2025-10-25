from typing import Sequence
from uuid import UUID

from domain.coin import Coins
from domain.error import DomainError
from domain.weapon.damage import WeaponDamage
from domain.weight import Weight


class Weapon:
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
    ) -> None:
        self.__validate_name(name)
        self.__validate_description(description)
        self.__validate_properties(weapon_properties)
        self.__weapon_id = weapon_id
        self.__kind = weapon_kind
        self.__name = name
        self.__description = description
        self.__cost = cost
        self.__damage = damage
        self.__weight = weight
        self.__properties = list(weapon_properties)

    def weapon_id(self) -> UUID:
        return self.__weapon_id

    def kind(self) -> UUID:
        return self.__kind

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def cost(self) -> Coins:
        return self.__cost

    def damage(self) -> WeaponDamage:
        return self.__damage

    def weight(self) -> Weight:
        return self.__weight

    def properties(self) -> list[UUID]:
        return self.__properties

    def new_kind(self, kind: UUID) -> None:
        if self.__kind == kind:
            raise DomainError.idempotent("текущий вид оружия равен новому виду")
        self.__kind = kind

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название оружия равно новому названию"
            )
        self.__validate_name(name)
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

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

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название оружия не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название оружия не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание оружия не может быть пустым")

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
