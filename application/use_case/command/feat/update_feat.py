from application.dto.command.feat import UpdateFeatCommand
from application.dto.model.feat import AppFeat
from application.repository import FeatRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.armor import ArmorType
from domain.error import DomainError
from domain.feat import FeatRequiredModifier, FeatService
from domain.modifier import Modifier


class UpdateFeatUseCase(UserCheck):
    def __init__(
        self,
        feat_service: FeatService,
        user_repository: UserRepository,
        feat_repository: FeatRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__feat_service = feat_service
        self.__feat_repository = feat_repository

    async def execute(self, command: UpdateFeatCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__feat_repository.id_exists(command.feat_id):
            raise DomainError.not_found(f"черты с id {command.feat_id} не существует")
        app_feat = await self.__feat_repository.get_by_id(command.feat_id)
        feat = app_feat.to_domain()
        if command.name is not None:
            if not await self.__feat_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"не возможно переименовать черту с названием {command.name}"
                )
            feat.new_name(command.name)
        if command.description is not None:
            feat.new_description(command.description)
        if command.caster is not None:
            feat.new_is_caster(command.caster)
        if command.required_armor_types is not None:
            feat.new_required_armor_types(
                [
                    ArmorType.from_str(required_armor_type)
                    for required_armor_type in command.required_armor_types
                ]
            )
        if command.required_modifiers is not None:
            feat.new_required_modifiers(
                [
                    FeatRequiredModifier(
                        Modifier.from_str(required_modifier.modifier),
                        required_modifier.min_value,
                    )
                    for required_modifier in command.required_modifiers
                ]
            )
        if command.increase_modifiers is not None:
            feat.new_increase_modifiers(
                [
                    Modifier.from_str(increase_modifier)
                    for increase_modifier in command.increase_modifiers
                ]
            )
        await self.__feat_repository.update(AppFeat.from_domain(feat))
