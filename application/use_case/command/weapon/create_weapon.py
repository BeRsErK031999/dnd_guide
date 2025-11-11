from application.dto.command.weapon import CreateWeaponCommand
from application.repository import (
    MaterialRepository,
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
from domain.weapon import Weapon, WeaponDamage, WeaponService
from domain.weight import Weight, WeightUnit


class CreateWeaponUseCase(UserCheck):
    def __init__(
        self,
        weapon_service: WeaponService,
        user_repository: UserRepository,
        weapon_repository: WeaponRepository,
        kind_repository: WeaponKindRepository,
        property_repository: WeaponPropertyRepository,
        material_repository: MaterialRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__weapon_service = weapon_service
        self.__weapon_repository = weapon_repository
        self.__kind_repository = kind_repository
        self.__property_repository = property_repository
        self.__material_repository = material_repository

    async def execute(self, command: CreateWeaponCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__weapon_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"оружие с названием {command.name} не возможно создать"
            )
        if not await self.__kind_repository.id_exists(command.weapon_kind):
            raise DomainError.invalid_data(
                f"тип оружия с id {command.weapon_kind} не существует"
            )
        for property_id in command.weapon_properties:
            if not await self.__property_repository.id_exists(property_id):
                raise DomainError.invalid_data(
                    f"свойство оружия с id {property_id} не существует"
                )
        if not await self.__material_repository.id_exists(command.material_id):
            raise DomainError.invalid_data(
                f"материал с id {command.material_id} не существует"
            )
        weapon = Weapon(
            await self.__weapon_repository.next_id(),
            command.weapon_kind,
            command.name,
            command.description,
            Coins(command.cost.count, PieceType.from_str(command.cost.piece_type)),
            WeaponDamage(
                Dice(
                    command.damage.dice.count,
                    DiceType.from_str(command.damage.dice.dice_type),
                ),
                DamageType.from_str(command.damage.damage_type),
                command.damage.bonus_damage,
            ),
            Weight(command.weight.count, WeightUnit.from_str(command.weight.unit)),
            command.weapon_properties,
            command.material_id,
        )
        await self.__weapon_repository.save(weapon)
