from uuid import UUID

from domain.error import DomainError
from domain.subrace.increase_modifier import SubraceIncreaseModifier


class Subrace:
    def __init__(
        self,
        subrace_id: UUID,
        race_id: UUID,
        name: str,
        description: str,
        increase_modifier: SubraceIncreaseModifier,
    ) -> None:
        self.__validate_name(name)
        self.__validate_description(description)
        self.__subrace_id = subrace_id
        self.__race_id = race_id
        self.__name = name
        self.__description = description
        self.__increase_modifier = increase_modifier

    def subrace_id(self) -> UUID:
        return self.__subrace_id

    def race_id(self) -> UUID:
        return self.__race_id

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def increase_modifier(self) -> SubraceIncreaseModifier:
        return self.__increase_modifier

    def new_race_id(self, race_id: UUID) -> None:
        if self.__race_id == race_id:
            raise DomainError.idempotent("текущая раса ровна новой расе")
        self.__race_id = race_id

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название подрасы равно новому названию подрасы"
            )
        self.__validate_name(name)
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def new_increase_modifier(self, increase_modifier: SubraceIncreaseModifier) -> None:
        if self.__increase_modifier == increase_modifier:
            raise DomainError.idempotent(
                "текущее увеличение характеристик подрасы равно новому увеличению характеристик подрасы"
            )
        self.__increase_modifier = increase_modifier

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название подрасы не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название подрасы не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание подрасы не может быть пустым")

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__subrace_id == value.__subrace_id
        if isinstance(value, UUID):
            return self.__subrace_id == value
        raise NotImplemented
