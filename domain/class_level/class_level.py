from uuid import UUID

from domain.class_level.damage import ClassLevelBonusDamage
from domain.class_level.dice import ClassLevelDice
from domain.class_level.points import ClassLevelPoints
from domain.class_level.spell_slots import ClassLevelSpellSlots
from domain.error import DomainError
from domain.length import Length


class ClassLevel:
    def __init__(
        self,
        level_id: UUID,
        class_id: UUID,
        level: int,
        dice: ClassLevelDice | None,
        spell_slots: ClassLevelSpellSlots | None,
        number_cantrips_know: int | None,
        number_spells_know: int | None,
        number_arcanums_know: int | None,
        points: ClassLevelPoints | None,
        bonus_damage: ClassLevelBonusDamage | None,
        increase_speed: Length | None,
    ) -> None:
        self.__validate_level(level)
        self.__level_id = level_id
        self.__class_id = class_id
        self.__level = level
        self.__dice = dice
        self.__spell_slots = spell_slots
        self.__number_cantrips_know = number_cantrips_know
        self.__number_spells_know = number_spells_know
        self.__number_arcanums_know = number_arcanums_know
        self.__points = points
        self.__bonus_damage = bonus_damage
        self.__increase_speed = increase_speed

    def level_id(self) -> UUID:
        return self.__level_id

    def class_id(self) -> UUID:
        return self.__class_id

    def level(self) -> int:
        return self.__level

    def dice(self) -> ClassLevelDice | None:
        return self.__dice

    def spell_slots(self) -> ClassLevelSpellSlots | None:
        return self.__spell_slots

    def number_cantrips_know(self) -> int | None:
        return self.__number_cantrips_know

    def number_spells_know(self) -> int | None:
        return self.__number_spells_know

    def number_arcanums_know(self) -> int | None:
        return self.__number_arcanums_know

    def points(self) -> ClassLevelPoints | None:
        return self.__points

    def bonus_damage(self) -> ClassLevelBonusDamage | None:
        return self.__bonus_damage

    def increase_speed(self) -> Length | None:
        return self.__increase_speed

    def new_class_id(self, class_id: UUID) -> None:
        if self.__class_id == class_id:
            raise DomainError.idempotent("текущий класс равен новому")
        self.__class_id = class_id

    def new_level(self, level: int) -> None:
        if self.__level == level:
            raise DomainError.idempotent("текущий уровень равен новому")
        self.__validate_level(level)
        self.__level = level

    def new_dice(self, dice: ClassLevelDice | None) -> None:
        if self.__dice == dice:
            raise DomainError.idempotent(
                "текущие особенности связанные с костью равны новым"
            )
        self.__dice = dice

    def new_spell_slots(self, spell_slots: ClassLevelSpellSlots | None) -> None:
        if self.__spell_slots == spell_slots:
            raise DomainError.idempotent("текущие ячейки заклинаний равны новым")
        self.__spell_slots = spell_slots

    def new_number_cantrips_know(self, number_cantrips_know: int | None) -> None:
        if self.__number_cantrips_know == number_cantrips_know:
            raise DomainError.idempotent(
                "количество текущих известных заговоров равно новым"
            )
        self.__number_cantrips_know = number_cantrips_know

    def new_number_spells_know(self, number_spells_know: int | None) -> None:
        if self.__number_spells_know == number_spells_know:
            raise DomainError.idempotent(
                "количество текущих известных заклинаний равны новым"
            )
        self.__number_spells_know = number_spells_know

    def new_number_arcanums_know(self, number_arcanums_know: int | None) -> None:
        if self.__number_arcanums_know == number_arcanums_know:
            raise DomainError.idempotent(
                "количество текущих известных воззваний равны новым"
            )
        self.__number_arcanums_know = number_arcanums_know

    def new_points(self, points: ClassLevelPoints | None) -> None:
        if self.__points == points:
            raise DomainError.idempotent("текущие бонусные очки равны новым")
        self.__points = points

    def new_bonus_damage(self, bonus_damage: ClassLevelBonusDamage | None) -> None:
        if self.__bonus_damage == bonus_damage:
            raise DomainError.idempotent("текущий бонусный урон равен новому")
        self.__bonus_damage = bonus_damage

    def new_increase_speed(self, increase_speed: Length | None) -> None:
        if self.__increase_speed == increase_speed:
            raise DomainError.idempotent("текущее увеличение скорости равно новому")
        self.__increase_speed = increase_speed

    def __validate_level(self, level: int) -> None:
        if level < 1 or level > 20:
            raise DomainError.invalid_data(
                "уровень класса должен находиться в диапазоне от 1 до 20"
            )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__level_id == value.__level_id
        if isinstance(value, UUID):
            return self.__level_id == value
        raise NotImplemented
