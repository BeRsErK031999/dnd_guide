from application.dto.command.armor import CreateArmorCommand
from application.repository import ArmorRepository, MaterialRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.armor import Armor, ArmorClass, ArmorService, ArmorType
from domain.coin import Coins, PieceType
from domain.error import DomainError
from domain.modifier import Modifier
from domain.weight import Weight, WeightUnit


class CreateArmorUseCase(UserCheck):
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

    async def execute(self, command: CreateArmorCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__armor_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать доспехи с названием {command.name}"
            )
        if not await self.__material_repository.id_exists(command.material_id):
            raise DomainError.invalid_data(
                f"материал с id {command.material_id} не существует"
            )
        armor = Armor(
            await self.__armor_repository.next_id(),
            ArmorType.from_str(command.armor_type),
            command.name,
            command.description,
            ArmorClass(
                command.armor_class.base_class,
                (
                    None
                    if command.armor_class.modifier is None
                    else Modifier.from_str(command.armor_class.modifier)
                ),
                command.armor_class.max_modifier_bonus,
            ),
            command.strength,
            command.stealth,
            Weight(command.weight.count, WeightUnit.from_str(command.weight.unit)),
            Coins(command.cost.count, PieceType.from_str(command.cost.piece_type)),
            command.material_id,
        )
        await self.__armor_repository.create(armor)
