from typing import Sequence
from uuid import UUID

from domain.character_class.hit import ClassHits
from domain.character_class.name import ClassName
from domain.character_class.proficiency import ClassProficiencies
from domain.error import DomainError
from domain.modifier import Modifier


class CharacterClass:
    def __init__(
        self,
        class_id: UUID,
        name: ClassName,
        description: str,
        primary_modifiers: Sequence[Modifier],
        hits: ClassHits,
        proficiencies: ClassProficiencies,
    ) -> None:
        self.__validate_description(description)
        self.__validate_primary_modifiers(primary_modifiers)
        self.__class_id = class_id
        self.__name = name
        self.__description = description
        self.__primary_modifiers = list(primary_modifiers)
        self.__hits = hits
        self.__proficiencies = proficiencies

    def class_id(self) -> UUID:
        return self.__class_id

    def name(self) -> ClassName:
        return self.__name

    def description(self) -> str:
        return self.__description

    def primary_modifier(self) -> list[Modifier]:
        return self.__primary_modifiers

    def hits(self) -> ClassHits:
        return self.__hits

    def proficiency(self) -> ClassProficiencies:
        return self.__proficiencies

    def new_name(self, name: ClassName) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название класса равно новому названию класса"
            )
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def new_primary_modifiers(self, primary_modifiers: Sequence[Modifier]) -> None:
        if set(self.__primary_modifiers) == set(primary_modifiers):
            raise DomainError.idempotent(
                "текущий список главных модификаторов равен списку новых главных модификаторов"
            )
        self.__validate_primary_modifiers(primary_modifiers)
        self.__primary_modifiers = list(primary_modifiers)

    def new_hits(self, hits: ClassHits) -> None:
        if self.__hits == hits:
            raise DomainError.idempotent("текущие хиты равны новым хитам")
        self.__hits = hits

    def new_proficiencies(self, proficiencies: ClassProficiencies) -> None:
        if self.__proficiencies == proficiencies:
            raise DomainError.idempotent("текущее владение равно новому владению")
        self.__proficiencies = proficiencies

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание класса не может быть пустым")

    def __validate_primary_modifiers(self, modifiers: Sequence[Modifier]) -> None:
        if len(modifiers) < 1:
            raise DomainError.invalid_data(
                "количество главных модификаторов класса не может быть меньше 1"
            )
        if len(modifiers) != len(set(modifiers)):
            raise DomainError.invalid_data(
                "список главных модификаторов класса содержит дубликаты"
            )

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__class_id == value.__class_id
        if isinstance(value, UUID):
            return self.__class_id == value
        raise NotImplemented
