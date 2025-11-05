from application.dto.command.weapon_property import CreateWeaponPropertyCommand
from application.repository import UserRepository, WeaponPropertyRepository
from application.use_case.command.user_check import UserCheck
from domain.dice import Dice
from domain.error import DomainError
from domain.length import Length, LengthUnit
from domain.weapon_property import (
    WeaponProperty,
    WeaponPropertyName,
    WeaponPropertyService,
)


class CreateWeaponPropertyUseCase(UserCheck):
    def __init__(
        self,
        weapon_property_service: WeaponPropertyService,
        user_repository: UserRepository,
        weapon_property_repository: WeaponPropertyRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__property_service = weapon_property_service
        self.__property_repository = weapon_property_repository

    async def execute(self, command: CreateWeaponPropertyCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__property_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"свойство с именем {command.name} не возможно создать"
            )
        weapon_property = WeaponProperty(
            await self.__property_repository.next_id(),
            WeaponPropertyName.from_str(command.name),
            command.description,
            (
                Length(
                    command.base_range.range.count,
                    LengthUnit(command.base_range.range.unit),
                )
                if command.base_range is not None
                and command.base_range.range is not None
                else None
            ),
            (
                Length(
                    command.max_range.range.count,
                    LengthUnit(command.max_range.range.unit),
                )
                if command.max_range is not None and command.max_range.range is not None
                else None
            ),
            (
                Dice(command.second_hand_dice.dice)
                if command.second_hand_dice is not None
                and command.second_hand_dice.dice is not None
                else None
            ),
        )
        await self.__property_repository.save(weapon_property)
