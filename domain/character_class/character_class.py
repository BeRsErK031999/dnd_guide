from typing import Sequence
from uuid import UUID

from domain.character_class.hit import ClassHits
from domain.character_class.proficiency import ClassProficiencies
from domain.error import DomainError
from domain.mixin import (
    EntityDescription,
    EntityName,
    EntityNameInEnglish,
    EntitySource,
)
from domain.modifier import Modifier


class CharacterClass(EntityName, EntityNameInEnglish, EntityDescription, EntitySource):
    def __init__(
        self,
        class_id: UUID,
        name: str,
        description: str,
        primary_modifiers: Sequence[Modifier],
        hits: ClassHits,
        proficiencies: ClassProficiencies,
        name_in_english: str,
        source_id: UUID,
    ) -> None:
        self._validate_primary_modifiers(primary_modifiers)
        EntityDescription.__init__(self, description)
        EntityNameInEnglish.__init__(self, name_in_english)
        EntityName.__init__(self, name)
        EntitySource.__init__(self, source_id)
        self._class_id = class_id
        self._primary_modifiers = list(primary_modifiers)
        self._hits = hits
        self._proficiencies = proficiencies

    def class_id(self) -> UUID:
        return self._class_id

    def primary_modifiers(self) -> list[Modifier]:
        return self._primary_modifiers

    def hits(self) -> ClassHits:
        return self._hits

    def proficiency(self) -> ClassProficiencies:
        return self._proficiencies

    def new_primary_modifiers(self, primary_modifiers: Sequence[Modifier]) -> None:
        if set(self._primary_modifiers) == set(primary_modifiers):
            raise DomainError.idempotent(
                "текущий список главных модификаторов равен списку новых главных модификаторов"
            )
        self._validate_primary_modifiers(primary_modifiers)
        self._primary_modifiers = list(primary_modifiers)

    def new_hits(self, hits: ClassHits) -> None:
        if self._hits == hits:
            raise DomainError.idempotent("текущие хиты равны новым хитам")
        self._hits = hits

    def new_proficiencies(self, proficiencies: ClassProficiencies) -> None:
        if self._proficiencies == proficiencies:
            raise DomainError.idempotent("текущее владение равно новому владению")
        self._proficiencies = proficiencies

    def _validate_primary_modifiers(self, modifiers: Sequence[Modifier]) -> None:
        if len(modifiers) < 1:
            raise DomainError.invalid_data(
                "количество главных модификаторов класса не может быть меньше 1"
            )
        if len(modifiers) != len(set(modifiers)):
            raise DomainError.invalid_data(
                "список главных модификаторов класса содержит дубликаты"
            )

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._class_id == value._class_id
        if isinstance(value, UUID):
            return self._class_id == value
        raise NotImplemented
