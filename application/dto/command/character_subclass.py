from uuid import UUID

from domain.error import DomainError


class SubclassCreateCommand:
    def __init__(
        self,
        user_id: UUID,
        class_id: UUID,
        name: str,
        description: str,
    ) -> None:
        self.user_id = user_id
        self.class_id = class_id
        self.name = name
        self.description = description


class SubclassUpdateCommand:
    def __init__(
        self,
        user_id: UUID,
        subclass_id: UUID,
        class_id: UUID | None,
        name: str | None,
        description: str | None,
    ) -> None:
        if all([class_id is None, name is None, description is None]):
            raise DomainError.invalid_data(
                "не переданы данные для обновления подкласса"
            )
        self.user_id = user_id
        self.subclass_id = subclass_id
        self.class_id = class_id
        self.name = name
        self.description = description


class SubclassDeleteCommand:
    def __init__(
        self,
        user_id: UUID,
        subclass_id: UUID,
    ) -> None:
        self.user_id = user_id
        self.subclass_id = subclass_id
