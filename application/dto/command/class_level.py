from typing import Sequence
from uuid import UUID

from domain.error import DomainError


class CreateClassLevelCommand:
    def __init__(
        self,
        user_id: UUID,
        class_id: UUID,
        level: int,
        dice: str | None,
        dice_description: str | None,
        number_dices: int | None,
        spell_slots: Sequence[int] | None,
        number_cantrips_know: int | None,
        number_spells_know: int | None,
        number_arcanums_know: int | None,
        points: int | None,
        points_description: str | None,
        bonus_damage: int | None,
        bonus_damage_description: str | None,
        increase_speed: int | None,
        increase_speed_unit: str | None,
        increase_speed_description: str | None,
    ) -> None:
        if any(
            [dice is not None, dice_description is not None, number_dices is not None]
        ) and not all([dice is not None, dice_description is not None]):
            raise DomainError.invalid_data(
                "для указания кости в уровне класса необходимо передать кость, ее "
                "описание и опционально их количество(если она всегда одна, то "
                "количество передавать не нужно)"
            )
        if any([points is not None, points_description is not None]) and not all(
            [points is not None, points_description is not None]
        ):
            raise DomainError.invalid_data(
                "для указания дополнительных очков необходимо передать их количество и "
                "описание"
            )
        if any(
            [bonus_damage is not None, bonus_damage_description is not None]
        ) and not all([bonus_damage is not None, bonus_damage_description is not None]):
            raise DomainError.invalid_data(
                "для указания дополнительного урона необходимо передать бонусный урон и "
                "его описание"
            )
        if any(
            [
                increase_speed is not None,
                increase_speed_unit is not None,
                increase_speed_description is not None,
            ]
        ) and not all(
            [
                increase_speed is not None,
                increase_speed_unit is not None,
                increase_speed_description is not None,
            ]
        ):
            raise DomainError.invalid_data(
                "для указания увеличения скорости нужно передать количество, единицу "
                "измерения и описание"
            )
        self.user_id = user_id
        self.class_id = class_id
        self.level = level
        self.dice = dice
        self.dice_description = dice_description
        self.number_dices = number_dices
        self.spell_slots = spell_slots
        self.number_cantrips_know = number_cantrips_know
        self.number_spells_know = number_spells_know
        self.number_arcanums_know = number_arcanums_know
        self.points = points
        self.points_description = points_description
        self.bonus_damage = bonus_damage
        self.bonus_damage_description = bonus_damage_description
        self.increase_speed = increase_speed
        self.increase_speed_unit = increase_speed_unit
        self.increase_speed_description = increase_speed_description


class UpdateClassLevelCommand:
    def __init__(
        self,
        user_id: UUID,
        class_level_id: UUID,
        class_id: UUID | None,
        level: int | None,
        dice: str | None,
        dice_description: str | None,
        number_dices: int | None,
        spell_slots: Sequence[int] | None,
        number_cantrips_know: int | None,
        number_spells_know: int | None,
        number_arcanums_know: int | None,
        points: int | None,
        points_description: str | None,
        bonus_damage: int | None,
        bonus_damage_description: str | None,
        increase_speed: int | None,
        increase_speed_unit: str | None,
        increase_speed_description: str | None,
    ) -> None:
        if any(
            [dice is not None, dice_description is not None, number_dices is not None]
        ) and not all([dice is not None, dice_description is not None]):
            raise DomainError.invalid_data(
                "для указания кости в уровне класса необходимо передать кость, ее "
                "описание и опционально их количество(если она всегда одна, то "
                "количество передавать не нужно)"
            )
        if any([points is not None, points_description is not None]) and not all(
            [points is not None, points_description is not None]
        ):
            raise DomainError.invalid_data(
                "для указания дополнительных очков необходимо передать их количество и "
                "описание"
            )
        if any(
            [bonus_damage is not None, bonus_damage_description is not None]
        ) and not all([bonus_damage is not None, bonus_damage_description is not None]):
            raise DomainError.invalid_data(
                "для указания дополнительного урона необходимо передать бонусный урон и "
                "его описание"
            )
        if any(
            [
                increase_speed is not None,
                increase_speed_unit is not None,
                increase_speed_description is not None,
            ]
        ) and not all(
            [
                increase_speed is not None,
                increase_speed_unit is not None,
                increase_speed_description is not None,
            ]
        ):
            raise DomainError.invalid_data(
                "для указания увеличения скорости нужно передать количество, единицу "
                "измерения и описание"
            )
        self.user_id = user_id
        self.class_level_id = class_level_id
        self.class_id = class_id
        self.level = level
        self.dice = dice
        self.dice_description = dice_description
        self.number_dices = number_dices
        self.spell_slots = spell_slots
        self.number_cantrips_know = number_cantrips_know
        self.number_spells_know = number_spells_know
        self.number_arcanums_know = number_arcanums_know
        self.points = points
        self.points_description = points_description
        self.bonus_damage = bonus_damage
        self.bonus_damage_description = bonus_damage_description
        self.increase_speed = increase_speed
        self.increase_speed_unit = increase_speed_unit
        self.increase_speed_description = increase_speed_description


class DeleteClassLevelCommand:
    def __init__(self, user_id: UUID, class_level_id: UUID) -> None:
        self.user_id = user_id
        self.class_level_id = class_level_id
