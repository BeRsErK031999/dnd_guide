from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName
from domain.weapon_kind.weapon_type import WeaponType


class WeaponKind(EntityName, EntityDescription):
    def __init__(
        self,
        weapon_kind_id: UUID,
        name: str,
        description: str,
        weapon_type: WeaponType,
    ) -> None:
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self.__weapon_kind_id = weapon_kind_id
        self.__weapon_type = weapon_type

    def weapon_kind_id(self) -> UUID:
        return self.__weapon_kind_id

    def weapon_type(self) -> WeaponType:
        return self.__weapon_type

    def new_weapon_type(self, weapon_type: WeaponType) -> None:
        if self.__weapon_type == weapon_type:
            raise DomainError.idempotent("текущий тип оружия идентичен новому типу")
        self.__weapon_type = weapon_type

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__weapon_kind_id == value.__weapon_kind_id
        if isinstance(value, UUID):
            return self.__weapon_kind_id == value
        raise NotImplemented
