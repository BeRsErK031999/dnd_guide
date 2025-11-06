from typing import Sequence
from uuid import UUID

from domain.error import DomainError
from domain.feat.required_modifier import FeatRequiredModifier
from domain.mixin import EntityDescription, EntityName
from domain.modifier import Modifier


class Feat(EntityName, EntityDescription):
    def __init__(
        self,
        feat_id: UUID,
        name: str,
        description: str,
        required_modifiers: Sequence[FeatRequiredModifier],
        increase_modifiers: Sequence[Modifier],
    ) -> None:
        self.__validate_duplicate_in_seq(
            required_modifiers, "обязательные модификаторы содержат дубликаты"
        )
        self.__validate_duplicate_in_seq(
            increase_modifiers, "увеличиваемые модификаторы содержат дубликаты"
        )
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self.__feat_id = feat_id
        self.__required_modifiers = list(required_modifiers)
        self.__increase_modifiers = list(increase_modifiers)

    def feat_id(self) -> UUID:
        return self.__feat_id

    def required_modifiers(self) -> Sequence[FeatRequiredModifier]:
        return self.__required_modifiers

    def increase_modifiers(self) -> Sequence[Modifier]:
        return self.__increase_modifiers

    def new_required_modifiers(
        self, required_modifiers: Sequence[FeatRequiredModifier]
    ) -> None:
        if set(self.__required_modifiers) == set(required_modifiers):
            raise DomainError.idempotent(
                "текущий набор обязательных модификаторов равен новому"
            )
        self.__validate_duplicate_in_seq(
            required_modifiers, "обязательные модификаторы содержат дубликаты"
        )
        self.__required_modifiers = list(required_modifiers)

    def new_increase_modifiers(self, increase_modifiers: Sequence[Modifier]) -> None:
        if set(self.__required_modifiers) == set(increase_modifiers):
            raise DomainError.idempotent(
                "текущий набор увеличиваемых модификаторов равен новому"
            )
        self.__validate_duplicate_in_seq(
            increase_modifiers, "увеличиваемые модификаторы содержат дубликаты"
        )
        self.__increase_modifiers = list(increase_modifiers)

    def __validate_duplicate_in_seq(self, seq: Sequence, msg: str) -> None:
        if len(seq) == 0:
            return
        if len(seq) != len(set(seq)):
            raise DomainError.invalid_data(msg)

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__feat_id == value.__feat_id
        if isinstance(value, UUID):
            return self.__feat_id == value
        raise NotImplemented
