from uuid import UUID

from domain.class_level.spell_slots import SpellSlots
from domain.dice import Dice
from domain.error import DomainError
from domain.length import Length


class ClassLevel:
    def __init__(
        self,
        level_id: UUID,
        class_id: UUID,
        dice: Dice | None,
        dice_description: str | None,
        number_dices: int | None,
        spell_slots: SpellSlots | None,
        number_cantrips_know: int | None,
        number_spells_know: int | None,
        number_arcanums_know: int | None,
        points: int | None,
        points_description: str | None,
        bonus_damage: int | None,
        bonus_damage_description: str | None,
        increase_speed: Length | None,
    ) -> None:
        if dice is not None and (
            dice_description is None or len(dice_description) == 0
        ):
            raise DomainError.invalid_data(
                "при указании кости необходимо ее функциональное описание"
            )
        if number_dices is not None and dice is None:
            raise DomainError.invalid_data(
                "при указании количества костей необходимо указать кость"
            )
        if points is not None and (
            points_description is None or len(points_description) == 0
        ):
            raise DomainError.invalid_data(
                "при указании очков необходимо указать их описание"
            )
        if bonus_damage is not None and (
            bonus_damage_description is None or len(bonus_damage_description) == 0
        ):
            raise DomainError.invalid_data(
                "при указании бонусного урона необходимо указать его описание"
            )
        self.__level_id = level_id
        self.__class_id = class_id
        self.__dice = dice
        self.__dice_description = dice_description
        self.__number_dices = number_dices
        self.__spell_slots = spell_slots
        self.__number_cantrips_know = number_cantrips_know
        self.__number_spells_know = number_spells_know
        self.__number_arcanums_know = number_arcanums_know
        self.__points = points
        self.__points_description = points_description
        self.__bonus_damage = bonus_damage
        self.__bonus_damage_description = bonus_damage_description
        self.__increase_speed = increase_speed

    def level_id(self) -> UUID:
        return self.__level_id

    def class_id(self) -> UUID:
        return self.__class_id

    def dice(self) -> Dice | None:
        return self.__dice

    def dice_description(self) -> str | None:
        return self.__dice_description

    def number_dices(self) -> int | None:
        return self.__number_dices

    def spell_slots(self) -> SpellSlots | None:
        return self.__spell_slots

    def number_cantrips_know(self) -> int | None:
        return self.__number_cantrips_know

    def number_spells_know(self) -> int | None:
        return self.__number_spells_know

    def number_arcanums_know(self) -> int | None:
        return self.__number_arcanums_know

    def points(self) -> int | None:
        return self.__points

    def points_description(self) -> str | None:
        return self.__points_description

    def bonus_damage(self) -> int | None:
        return self.__bonus_damage

    def bonus_damage_description(self) -> str | None:
        return self.__bonus_damage_description

    def increase_speed(self) -> Length | None:
        return self.__increase_speed

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__level_id == value.__level_id
        if isinstance(value, UUID):
            return self.__level_id == value
        raise NotImplemented
