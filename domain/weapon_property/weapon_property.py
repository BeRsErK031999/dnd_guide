from uuid import UUID

from domain.dice import Dice
from domain.error import DomainError
from domain.length import Length
from domain.mixin import EntityDescription
from domain.weapon_property.name import WeaponPropertyName


class WeaponProperty(EntityDescription):
    def __init__(
        self,
        weapon_property_id: UUID,
        name: WeaponPropertyName,
        description: str,
        base_range: Length | None,
        max_range: Length | None,
        second_hand_dice: Dice | None,
    ) -> None:
        self.__validate_stats_by_name(name, base_range, max_range, second_hand_dice)
        EntityDescription.__init__(self, description)
        self.__weapon_property_id = weapon_property_id
        self.__name = name
        self.__base_range = base_range
        self.__max_range = max_range
        self.__second_hand_dice = second_hand_dice

    def weapon_property_id(self) -> UUID:
        return self.__weapon_property_id

    def name(self) -> WeaponPropertyName:
        return self.__name

    def base_range(self) -> Length | None:
        return self.__base_range

    def max_range(self) -> Length | None:
        return self.__max_range

    def second_hand_dice(self) -> Dice | None:
        return self.__second_hand_dice

    def new_name(
        self,
        name: WeaponPropertyName,
        base_range: Length | None = None,
        max_range: Length | None = None,
        second_hand_dice: Dice | None = None,
    ) -> None:
        if self.__name == name:
            raise DomainError.idempotent("текущее название равно новому названию")
        self.__validate_stats_by_name(name, base_range, max_range, second_hand_dice)
        self.__name = name
        self.__base_range = base_range
        self.__max_range = max_range
        self.__second_hand_dice = second_hand_dice

    def new_base_range(self, base_range: Length | None) -> None:
        if self.__name != WeaponPropertyName.AMMUNITION:
            raise DomainError.invalid_data(
                "для этого свойства нельзя назначить базовую дистанцию"
            )
        if self.__base_range == base_range:
            raise DomainError.idempotent(
                "текущий базовый радиус равен новому базовому радиусу"
            )
        if (
            self.__max_range is not None
            and base_range is not None
            and self.__max_range < base_range
        ):
            raise DomainError.invalid_data(
                "базовый радиус атаки не может быть больше максимального"
            )
        self.__base_range = base_range

    def new_max_range(self, max_range: Length | None) -> None:
        if self.__name != WeaponPropertyName.AMMUNITION:
            raise DomainError.invalid_data(
                "для этого свойства нельзя назначить максимальную дистанцию"
            )
        if self.__max_range == max_range:
            raise DomainError.idempotent(
                "текущий максимальный радиус равен новому максимальному радиусу"
            )
        if (
            self.__base_range is not None
            and max_range is not None
            and self.__base_range > max_range
        ):
            raise DomainError.invalid_data(
                "максимальный радиус атаки не может быть меньше базового"
            )
        self.__max_range = max_range

    def new_second_hand_dice(self, dice: Dice) -> None:
        if self.__name != WeaponPropertyName.VERSATILE:
            raise DomainError.invalid_data(
                "для этого свойства нельзя назначить кость для двух рук"
            )
        if self.__second_hand_dice == dice:
            raise DomainError.idempotent(
                "текущая кость для второй руки ровна новой кости для второй руки"
            )
        self.__second_hand_dice = dice

    def __validate_stats_by_name(
        self,
        name: WeaponPropertyName,
        base_range: Length | None,
        max_range: Length | None,
        second_hand_dice: Dice | None,
    ):
        match name:
            case WeaponPropertyName.AMMUNITION:
                if base_range is None or max_range is None:
                    raise DomainError.invalid_data(
                        "для дистанционного оружия необходимо указать "
                        "базовую и максимальную дистанцию атаки"
                    )
                if second_hand_dice is not None:
                    raise DomainError.invalid_data(
                        "для дистанционного оружия нельзя указать кость "
                        "для второй руки"
                    )
            case WeaponPropertyName.VERSATILE:
                if base_range is not None or max_range is not None:
                    raise DomainError.invalid_data(
                        "для этого свойства нельзя указать базовый и максимальный "
                        "радиус атаки"
                    )
                if second_hand_dice is None:
                    raise DomainError.invalid_data(
                        "для универсального оружия необходимо указать урон "
                        "при удержании оружия двумя руками"
                    )
            case _:
                if (
                    base_range is not None
                    or max_range is not None
                    or second_hand_dice is not None
                ):
                    raise DomainError.invalid_data(
                        "для этого свойства нельзя указать базовый и "
                        "максимальный радиус атаки, а так же нельзя "
                        "указать урон при удержании оружия в двух руках"
                    )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__weapon_property_id == value.__weapon_property_id
        if isinstance(value, UUID):
            return self.__weapon_property_id == value
        raise NotImplemented
