from application.dto.command.class_level import UpdateClassLevelCommand
from application.dto.model.class_level import AppClassLevel
from application.repository import ClassLevelRepository, ClassRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.class_level import (
    ClassLevelBonusDamage,
    ClassLevelDice,
    ClassLevelIncreaseSpeed,
    ClassLevelPoints,
    ClassLevelService,
    ClassLevelSpellSlots,
)
from domain.dice import Dice, DiceType
from domain.error import DomainError
from domain.length import Length, LengthUnit


class UpdateClassLevelUseCase(UserCheck):
    def __init__(
        self,
        class_level_service: ClassLevelService,
        user_repository: UserRepository,
        class_level_repository: ClassLevelRepository,
        class_repository: ClassRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._class_level_service = class_level_service
        self._class_level_repository = class_level_repository
        self._class_repository = class_repository

    async def execute(self, command: UpdateClassLevelCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._class_level_repository.id_exists(command.class_level_id):
            raise DomainError.not_found(
                f"уровень с id {command.class_level_id} не существует"
            )
        app_class_level = await self._class_level_repository.get_by_id(
            command.class_level_id
        )
        class_level = app_class_level.to_domain()
        if command.class_id is not None and command.level is not None:
            if not await self._class_repository.id_exists(command.class_id):
                raise DomainError.invalid_data(
                    f"класс с id {command.class_id} не существует"
                )
            if not await self._class_level_service.can_create_with_class_and_level(
                command.class_id, command.level
            ):
                raise DomainError.invalid_data(
                    "для класса невозможно создать указанный уровень"
                )
            class_level.new_class_id(command.class_id)
            class_level.new_level(command.level)
        if command.class_id is not None:
            if not await self._class_repository.id_exists(command.class_id):
                raise DomainError.invalid_data(
                    f"класс с id {command.class_id} не существует"
                )
            if not await self._class_level_service.can_create_with_class_and_level(
                command.class_id, class_level.level()
            ):
                raise DomainError.invalid_data(
                    "для класса невозможно создать указанный уровень"
                )
            class_level.new_class_id(command.class_id)
        if command.level is not None:
            if not await self._class_level_service.can_create_with_class_and_level(
                class_level.class_id(), command.level
            ):
                raise DomainError.invalid_data(
                    "для класса невозможно создать указанный уровень"
                )
            class_level.new_level(command.level)
        if command.dice is not None:
            class_level.new_dice(
                ClassLevelDice(
                    Dice(
                        command.dice.dice.count,
                        DiceType.from_str(command.dice.dice.dice_type),
                    ),
                    command.dice.description,
                )
            )
        if command.spell_slots is not None:
            class_level.new_spell_slots(ClassLevelSpellSlots(command.spell_slots))
        if command.points is not None:
            class_level.new_points(
                ClassLevelPoints(command.points.points, command.points.description)
            )
        if command.bonus_damage is not None:
            class_level.new_bonus_damage(
                ClassLevelBonusDamage(
                    command.bonus_damage.damage, command.bonus_damage.description
                )
            )
        if command.increase_speed is not None:
            class_level.new_increase_speed(
                ClassLevelIncreaseSpeed(
                    Length(
                        command.increase_speed.speed.count,
                        LengthUnit.from_str(command.increase_speed.speed.unit),
                    ),
                    command.increase_speed.description,
                )
            )
        if command.number_cantrips_know is not None:
            class_level.new_number_cantrips_know(command.number_cantrips_know)
        if command.number_spells_know is not None:
            class_level.new_number_spells_know(command.number_spells_know)
        if command.number_arcanums_know is not None:
            class_level.new_number_arcanums_know(command.number_arcanums_know)
        await self._class_level_repository.save(AppClassLevel.from_domain(class_level))
