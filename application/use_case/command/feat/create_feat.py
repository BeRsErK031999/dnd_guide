from application.dto.command.feat import CreateFeatCommand
from application.repository import FeatRepository, UserRepository
from application.use_case.command.user_check import UserCheck
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
        self.__user_check(command.user_id)
        if not await self.__feat_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать черту с названием {command.name}"
            )
        feat = Feat(
            await self.__feat_repository.next_id(),
            command.name,
            command.description,
            [
                FeatRequiredModifier(
                    Modifier.from_str(required_modifier.modifier),
                    required_modifier.min_value,
                )
                for required_modifier in command.required_modifiers
            ],
            [
                Modifier.from_str(increase_modifier)
                for increase_modifier in command.increase_modifiers
            ],
        )
        await self.__feat_repository.save(feat)
