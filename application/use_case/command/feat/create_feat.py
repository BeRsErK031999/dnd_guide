from application.dto.command.feat import CreateFeatCommand
from application.repository import FeatRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.armor import ArmorType
from domain.error import DomainError
from domain.feat import Feat, FeatRequiredModifier, FeatService
from domain.modifier import Modifier


class CreateFeatUseCase(UserCheck):
    def __init__(
        self,
        feat_service: FeatService,
        user_repository: UserRepository,
        feat_repository: FeatRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__feat_service = feat_service
        self.__feat_repository = feat_repository

    async def execute(self, command: CreateFeatCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__feat_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать черту с названием {command.name}"
            )
        feat = Feat(
            feat_id=await self.__feat_repository.next_id(),
            name=command.name,
            description=command.description,
            is_caster=command.is_caster,
            required_armor_types=[
                ArmorType.from_str(at) for at in command.required_armor_types
            ],
            required_modifiers=[
                FeatRequiredModifier(
                    Modifier.from_str(required_modifier.modifier),
                    required_modifier.min_value,
                )
                for required_modifier in command.required_modifiers
            ],
            increase_modifiers=[
                Modifier.from_str(increase_modifier)
                for increase_modifier in command.increase_modifiers
            ],
        )
        await self.__feat_repository.create(feat)
