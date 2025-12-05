from application.dto.command.armor import UpdateArmorCommand
from application.dto.model.armor import AppArmor
from application.repository import ArmorRepository, MaterialRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.armor import ArmorClass, ArmorService, ArmorType
from domain.coin import Coins, PieceType
from domain.error import DomainError
from domain.modifier import Modifier
from domain.weight import Weight, WeightUnit


class UpdateArmorUseCase(UserCheck):
    def __init__(
        self,
        armor_service: ArmorService,
        user_repository: UserRepository,
        armor_repository: ArmorRepository,
        material_repository: MaterialRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__armor_service = armor_service
        self.__armor_repository = armor_repository
        self.__material_repository = material_repository

    async def execute(self, command: UpdateArmorCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__armor_repository.id_exists(command.armor_id):
            raise DomainError.not_found(
                f"доспехов с id {command.armor_id} не существует"
            )
        app_armor = await self.__armor_repository.get_by_id(command.armor_id)
        armor = app_armor.to_domain()
        if command.armor_type is not None:
            armor.new_armor_type(ArmorType.from_str(command.armor_type))
        if command.name is not None:
            if not await self.__armor_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"не возможно создать доспехи с названием {command.name}"
                )
            armor.new_name(command.name)
        if command.description is not None:
            armor.new_description(command.description)
        if command.armor_class is not None:
            armor.new_armor_class(
                ArmorClass(
                    command.armor_class.base_class,
                    (
                        None
                        if command.armor_class.modifier is None
                        else Modifier.from_str(command.armor_class.modifier)
                    ),
                    command.armor_class.max_modifier_bonus,
                )
            )
        if command.strength is not None:
            armor.new_strength(command.strength)
        if command.stealth is not None:
            armor.new_stealth(command.stealth)
        if command.weight is not None:
            armor.new_weight(
                Weight(command.weight.count, WeightUnit.from_str(command.weight.unit))
            )
        if command.cost is not None:
            armor.new_cost(
                Coins(command.cost.count, PieceType.from_str(command.cost.piece_type))
            )
        if command.material_id is not None:
            if not await self.__material_repository.id_exists(command.material_id):
                raise DomainError.invalid_data(
                    f"материал с id {command.material_id} не существует"
                )
            armor.new_material_id(command.material_id)
        await self.__armor_repository.update(AppArmor.from_domain(armor))
