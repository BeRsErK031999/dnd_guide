from uuid import UUID

from domain.class_level.damage import ClassLevelBonusDamage
from domain.class_level.dice import ClassLevelDice
from domain.class_level.increase_speed import ClassLevelIncreaseSpeed
from domain.class_level.points import ClassLevelPoints
from domain.class_level.spell_slots import ClassLevelSpellSlots
from domain.error import DomainError


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
        increase_speed: ClassLevelIncreaseSpeed | None,
    ) -> None:
        self._validate_level(level)
        self._level_id = level_id
        self._class_id = class_id
        self._level = level
        self._dice = dice
        self._spell_slots = spell_slots
        self._number_cantrips_know = number_cantrips_know
        self._number_spells_know = number_spells_know
        self._number_arcanums_know = number_arcanums_know
        self._points = points
        self._bonus_damage = bonus_damage
        self._increase_speed = increase_speed

    def level_id(self) -> UUID:
        return self._level_id

    def class_id(self) -> UUID:
        return self._class_id

    def level(self) -> int:
        return self._level

    def dice(self) -> ClassLevelDice | None:
        return self._dice

    def spell_slots(self) -> ClassLevelSpellSlots | None:
        return self._spell_slots

    def number_cantrips_know(self) -> int | None:
        return self._number_cantrips_know

    def number_spells_know(self) -> int | None:
        return self._number_spells_know

    def number_arcanums_know(self) -> int | None:
        return self._number_arcanums_know

    def points(self) -> ClassLevelPoints | None:
        return self._points

    def bonus_damage(self) -> ClassLevelBonusDamage | None:
        return self._bonus_damage

    def increase_speed(self) -> ClassLevelIncreaseSpeed | None:
        return self._increase_speed

    def new_class_id(self, class_id: UUID) -> None:
        if self._class_id == class_id:
            raise DomainError.idempotent("текущий класс равен новому")
        self._class_id = class_id

    def new_level(self, level: int) -> None:
        if self._level == level:
            raise DomainError.idempotent("текущий уровень равен новому")
        self._validate_level(level)
        self._level = level

    def new_dice(self, dice: ClassLevelDice | None) -> None:
        if self._dice == dice:
            raise DomainError.idempotent(
                "текущие особенности связанные с костью равны новым"
            )
        self._dice = dice

    def new_spell_slots(self, spell_slots: ClassLevelSpellSlots | None) -> None:
        if self._spell_slots == spell_slots:
            raise DomainError.idempotent("текущие ячейки заклинаний равны новым")
        self._spell_slots = spell_slots

    def new_number_cantrips_know(self, number_cantrips_know: int | None) -> None:
        if self._number_cantrips_know == number_cantrips_know:
            raise DomainError.idempotent(
                "количество текущих известных заговоров равно новым"
            )
        self._number_cantrips_know = number_cantrips_know

    def new_number_spells_know(self, number_spells_know: int | None) -> None:
        if self._number_spells_know == number_spells_know:
            raise DomainError.idempotent(
                "количество текущих известных заклинаний равны новым"
            )
        self._number_spells_know = number_spells_know

    def new_number_arcanums_know(self, number_arcanums_know: int | None) -> None:
        if self._number_arcanums_know == number_arcanums_know:
            raise DomainError.idempotent(
                "количество текущих известных воззваний равны новым"
            )
        self._number_arcanums_know = number_arcanums_know

    def new_points(self, points: ClassLevelPoints | None) -> None:
        if self._points == points:
            raise DomainError.idempotent("текущие бонусные очки равны новым")
        self._points = points

    def new_bonus_damage(self, bonus_damage: ClassLevelBonusDamage | None) -> None:
        if self._bonus_damage == bonus_damage:
            raise DomainError.idempotent("текущий бонусный урон равен новому")
        self._bonus_damage = bonus_damage

    def new_increase_speed(
        self, increase_speed: ClassLevelIncreaseSpeed | None
    ) -> None:
        if self._increase_speed == increase_speed:
            raise DomainError.idempotent("текущее увеличение скорости равно новому")
        self._increase_speed = increase_speed

    def _validate_level(self, level: int) -> None:
        if level < 1 or level > 20:
            raise DomainError.invalid_data(
                "уровень класса должен находиться в диапазоне от 1 до 20"
            )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._level_id == value._level_id
        if isinstance(value, UUID):
            return self._level_id == value
        raise NotImplemented
