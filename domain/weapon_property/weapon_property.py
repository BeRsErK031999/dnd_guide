from uuid import UUID

from domain.dice import Dice
from domain.error import DomainError
from domain.weapon_property.name import WeaponPropertyName


class WeaponProperty:
    def __init__(
        self,
        weapon_property_id: UUID,
        name: WeaponPropertyName,
        description: str,
        base_range: int | None = None,
        max_range: int | None = None,
        second_hand_dice: Dice | None = None,
    ) -> None:
        self.__validate_description(description)
        self.__weapon_property_id = weapon_property_id
        self.__name = name
        self.__description = description
        self.__base_range = base_range
        self.__max_range = max_range
        self.__second_hand_dice = second_hand_dice

    def weapon_property_id(self) -> UUID:
        return self.__weapon_property_id

    def name(self) -> WeaponPropertyName:
        return self.__name

    def description(self) -> str:
        return self.__description

    def base_range(self) -> int | None:
        return self.__base_range

    def max_range(self) -> int | None:
        return self.__max_range

    def second_hand_dice(self) -> Dice | None:
        return self.__second_hand_dice

    def new_name(self, name: WeaponPropertyName) -> None:
        if self.__name == name:
            raise DomainError.idempotent("текущее название равно новому названию")
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def new_base_range(self, base_range: int) -> None:
        if self.__name != WeaponPropertyName.AMMUNITION:
            raise DomainError.invalid_data(
                "для этого свойства нельзя назначить базовую дистанцию"
            )
        self.__base_range = base_range

    def new_max_range(self, max_range: int) -> None:
        if self.__name != WeaponPropertyName.AMMUNITION:
            raise DomainError.invalid_data(
                "для этого свойства нельзя назначить максимальную дистанцию"
            )
        self.__max_range = max_range

    def new_second_hand_dice(self, dice: Dice) -> None:
        if self.__name != WeaponPropertyName.VERSATILE:
            raise DomainError.invalid_data(
                "для этого свойства нельзя назначить кость для двух рук"
            )
        self.__second_hand_dice = dice

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data(
                "описание свойства оружия не может быть пустым"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__weapon_property_id == value.__weapon_property_id
        raise NotImplemented
