from application.dto.command.weapon import UpdateWeaponCommand
from application.repository import (
    UserRepository,
    WeaponKindRepository,
    WeaponPropertyRepository,
    WeaponRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.coin import Coins, PieceType
from domain.damage_type import DamageType
from domain.dice import Dice, DiceType
from domain.error import DomainError
from domain.weapon import WeaponDamage, WeaponService
from domain.weight import Weight, WeightUnit


class UpdateWeaponUseCase(UserCheck):
    def __init__(
        self,
        weapon_service: WeaponService,
        user_repository: UserRepository,
        weapon_repository: WeaponRepository,
        kind_repository: WeaponKindRepository,
        property_repository: WeaponPropertyRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__weapon_service = weapon_service
        self.__weapon_repository = weapon_repository
        self.__kind_repository = kind_repository
        self.__property_repository = property_repository

    async def execute(self, command: UpdateWeaponCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__weapon_repository.is_weapon_of_id_exist(command.weapon_id):
            raise DomainError.not_found(
                f"оружие с id {command.weapon_id} не существует"
            )
        weapon = await self.__weapon_repository.get_weapon_of_id(command.weapon_id)
        if command.weapon_kind is not None:
            if not await self.__kind_repository.is_weapon_kind_of_id_exist(
                command.weapon_kind
            ):
                raise DomainError.invalid_data(
                    f"тип оружия с id {command.weapon_kind} не существует"
                )
            weapon.new_kind(command.weapon_kind)
        if command.name is not None:
            if not await self.__weapon_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"не возможно переименовать оружие с названием {command.name}"
                )
            weapon.new_name(command.name)
        if command.description is not None:
            weapon.new_description(command.description)
        if command.cost is not None:
            weapon.new_cost(
                Coins(command.cost.count, PieceType.from_str(command.cost.piece_type))
            )
        if command.damage is not None:
            weapon.new_damage(
                WeaponDamage(
                    Dice(
                        command.damage.dice.count,
                        DiceType.from_str(command.damage.dice.dice_type),
                    ),
                    DamageType.from_str(command.damage.damage_type),
                    command.damage.bonus_damage,
                )
            )
        if command.weight is not None:
            weapon.new_weight(
                Weight(command.weight.count, WeightUnit.from_str(command.weight.unit))
            )
        if command.weapon_properties is not None:
            for property_id in command.weapon_properties:
                if not await self.__property_repository.is_weapon_property_of_id_exist(
                    property_id
                ):
                    raise DomainError.invalid_data(
                        f"свойство оружия с id {property_id} не существует"
                    )
            weapon.new_properties(command.weapon_properties)
        await self.__weapon_repository.save(weapon)
