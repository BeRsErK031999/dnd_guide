from uuid import UUID

from domain.error import DomainError
from domain.weapon_kind.weapon_type import WeaponType


class WeaponKind:
    def __init__(
        self,
        weapon_kind_id: UUID,
        weapon_type: WeaponType,
        name: str,
        description: str,
    ) -> None:
        self.__validate_name(name)
        self.__validate_description(description)
        self.__weapon_kind_id = weapon_kind_id
        self.__weapon_type = weapon_type
        self.__name = name
        self.__description = description

    def weapon_kind_id(self) -> UUID:
        return self.__weapon_kind_id

    def weapon_type(self) -> WeaponType:
        return self.__weapon_type

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def new_weapon_type(self, weapon_type: WeaponType) -> None:
        if self.__weapon_type == weapon_type:
            raise DomainError.idempotent("текущий тип оружия идентичен новому типу")
        self.__weapon_type = weapon_type

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent("текущее имя равно новому имени")
        self.__validate_name(name)
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название вида оружия не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название вида оружия не может содержать более 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание вида оружия не может быть пустым")

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__weapon_kind_id == value.__weapon_kind_id
        raise NotImplemented
