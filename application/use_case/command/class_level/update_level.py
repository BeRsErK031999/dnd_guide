from application.dto.command.class_level import UpdateClassLevelCommand
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
from domain.dice import Dice
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
        self.__class_level_service = class_level_service
        self.__class_level_repository = class_level_repository
        self.__class_repository = class_repository

    async def execute(self, command: UpdateClassLevelCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__class_level_repository.is_level_of_id_exist(
            command.class_level_id
        ):
            raise DomainError.not_found(
                f"уровень с id {command.class_level_id} не существует"
            )
        class_level = await self.__class_level_repository.get_level_of_id(
            command.class_level_id
        )
        if command.class_id is not None and command.level is not None:
            if not await self.__class_repository.is_class_of_id_exist(command.class_id):
                raise DomainError.invalid_data(
                    f"класс с id {command.class_id} не существует"
                )
            if not await self.__class_level_service.can_create_with_class_and_level(
                command.class_id, command.level
            ):
                raise DomainError.invalid_data(
                    "для класса невозможно создать указанный уровень"
                )
            class_level.new_class_id(command.class_id)
            class_level.new_level(command.level)
        if command.class_id is not None:
            if not await self.__class_repository.is_class_of_id_exist(command.class_id):
                raise DomainError.invalid_data(
                    f"класс с id {command.class_id} не существует"
                )
            if not await self.__class_level_service.can_create_with_class_and_level(
                command.class_id, class_level.level()
            ):
                raise DomainError.invalid_data(
                    "для класса невозможно создать указанный уровень"
                )
            class_level.new_class_id(command.class_id)
        if command.level is not None:
            if not await self.__class_level_service.can_create_with_class_and_level(
                class_level.class_id(), command.level
            ):
                raise DomainError.invalid_data(
                    "для класса невозможно создать указанный уровень"
                )
            class_level.new_level(command.level)
        if (
            command.dice is not None
            and command.dice_description is not None
            and command.number_dices is not None
        ):
            class_level.new_dice(
                ClassLevelDice(
                    Dice.from_str(command.dice),
                    command.dice_description,
                    command.number_dices,
                )
            )
        if command.spell_slots is not None:
            class_level.new_spell_slots(ClassLevelSpellSlots(command.spell_slots))
        if command.points is not None and command.points_description is not None:
            class_level.new_points(
                ClassLevelPoints(command.points, command.points_description)
            )
        if (
            command.bonus_damage is not None
            and command.bonus_damage_description is not None
        ):
            class_level.new_bonus_damage(
                ClassLevelBonusDamage(
                    command.bonus_damage, command.bonus_damage_description
                )
            )
        if (
            command.increase_speed is not None
            and command.increase_speed_description is not None
            and command.increase_speed_unit is not None
        ):
            class_level.new_increase_speed(
                ClassLevelIncreaseSpeed(
                    Length(
                        command.increase_speed,
                        LengthUnit.from_str(command.increase_speed_unit),
                    ),
                    command.increase_speed_description,
                )
            )
        if command.number_cantrips_know is not None:
            class_level.new_number_cantrips_know(command.number_cantrips_know)
        if command.number_spells_know is not None:
            class_level.new_number_spells_know(command.number_spells_know)
        if command.number_arcanums_know is not None:
            class_level.new_number_arcanums_know(command.number_arcanums_know)
        await self.__class_level_repository.save(class_level)
