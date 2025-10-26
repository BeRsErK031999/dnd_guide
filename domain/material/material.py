from uuid import UUID

from domain.error import DomainError


class Material:
    def __init__(
        self,
        material_id: UUID,
        name: str,
        description: str,
    ) -> None:
        self.__validate_name(name)
        self.__validate_description(description)
        self.__material_id = material_id
        self.__name = name
        self.__description = description

    def material_id(self) -> UUID:
        return self.__material_id

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название материала равно новому названию материала"
            )
        self.__validate_name(name)
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название материала не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название материала не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание материала не может быть пустым")
