from application.dto.command.source import DeleteSourceCommand
from application.repository import (
    ClassRepository,
    RaceRepository,
    SourceRepository,
    SpellRepository,
    UserRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteSourceUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        source_repository: SourceRepository,
        class_repository: ClassRepository,
        race_repository: RaceRepository,
        spell_repository: SpellRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._source_repository = source_repository
        self._class_repository = class_repository
        self._race_repository = race_repository
        self._spell_repository = spell_repository

    async def execute(self, command: DeleteSourceCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._source_repository.id_exists(command.source_id):
            raise DomainError.not_found(
                f"источника с id {command.source_id} не существует"
            )
        exists_classes = await self._class_repository.filter(
            filter_by_source_ids=[command.source_id]
        )
        if len(exists_classes) > 0:
            raise DomainError.invalid_data(
                "этот источник используют классы: "
                f"{", ".join(c.name for c in exists_classes)}"
            )
        exists_races = await self._race_repository.filter(
            filter_by_source_ids=[command.source_id]
        )
        if len(exists_races) > 0:
            raise DomainError.invalid_data(
                "этот источник используют расы: "
                f"{", ".join(c.name for c in exists_races)}"
            )
        exists_spells = await self._spell_repository.filter(
            filter_by_source_ids=[command.source_id]
        )
        if len(exists_spells) > 0:
            raise DomainError.invalid_data(
                "этот источник используют заклинания: "
                f"{", ".join(c.name for c in exists_spells)}"
            )
        await self._source_repository.delete(command.source_id)
