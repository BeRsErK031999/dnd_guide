from application.dto.command.weapon_property import UpdateWeaponPropertyCommand
from application.repository import UserRepository, WeaponPropertyRepository
from application.use_case.command.user_check import UserCheck
from domain.dice import Dice, DiceType
from domain.error import DomainError
from domain.length import Length, LengthUnit
from domain.weapon_property import WeaponPropertyName, WeaponPropertyService


class UpdateWeaponPropertyUseCase(UserCheck):
    def __init__(
        self,
        weapon_property_service: WeaponPropertyService,
        user_repository: UserRepository,
        weapon_property_repository: WeaponPropertyRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__property_service = weapon_property_service
        self.__property_repository = weapon_property_repository

    async def execute(self, command: UpdateWeaponPropertyCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__property_repository.id_exists(command.weapon_property_id):
            raise DomainError.not_found(
                f"свойство с id {command.weapon_property_id} не существует"
            )
        weapon_property = await self.__property_repository.get_by_id(
            command.weapon_property_id
        )
        if command.name is not None:
            if not await self.__property_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"свойство не возможно переименовать с названием {command.name}"
                )
            weapon_property.new_name(
                WeaponPropertyName.from_str(command.name),
                (
                    Length(
                        command.base_range.range.count,
                        LengthUnit(command.base_range.range.unit),
                    )
                    if command.base_range is not None
                    and command.base_range.range is not None
                    else weapon_property.base_range()
                ),
                (
                    Length(
                        command.max_range.range.count,
                        LengthUnit(command.max_range.range.unit),
                    )
                    if command.max_range is not None
                    and command.max_range.range is not None
                    else weapon_property.max_range()
                ),
                (
                    Dice(
                        command.second_hand_dice.dice.count,
                        DiceType.from_str(command.second_hand_dice.dice.dice_type),
                    )
                    if command.second_hand_dice is not None
                    and command.second_hand_dice.dice is not None
                    else weapon_property.second_hand_dice()
                ),
            )
        if command.description is not None:
            weapon_property.new_description(command.description)
        if command.base_range is not None:
            weapon_property.new_base_range(
                (
                    Length(
                        command.base_range.range.count,
                        LengthUnit(command.base_range.range.unit),
                    )
                    if command.base_range.range is not None
                    else None
                )
            )
        if command.max_range is not None:
            weapon_property.new_max_range(
                (
                    Length(
                        command.max_range.range.count,
                        LengthUnit(command.max_range.range.unit),
                    )
                    if command.max_range.range is not None
                    else None
                )
            )
        if command.second_hand_dice is not None:
            weapon_property.new_second_hand_dice(
                (
                    Dice(
                        command.second_hand_dice.dice.count,
                        DiceType.from_str(command.second_hand_dice.dice.dice_type),
                    )
                    if command.second_hand_dice.dice is not None
                    else None
                )
            )
        await self.__property_repository.save(weapon_property)
